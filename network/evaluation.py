import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import PIL
import cv2 as cv

from webscraper.face_extract import detect_faces, resize_image_to_square

def eval_on_folder(
    model, 
    transform_chain, 
    class_labels,
    test_data_dir: str, 
    eval_images_limit=100,
    save_prediction_image_name: str = None,
    device="cuda:0"
    ): 
    unseen_dataset_dir = test_data_dir
    unseen_dataset_list = [f for f in os.listdir(unseen_dataset_dir) if f.endswith((".png", ".jpg", ".jpeg"))]
    eval_images_count = len(unseen_dataset_list)

    print(f'{eval_images_count} images to evaulate on.')

    # Extract class labels from training dataset
    fig, ax = plt.subplots(eval_images_limit // 10, 10)
    fig.set_figheight((eval_images_limit // 10) * 3)
    fig.set_figwidth(25)

    model.eval()

    for ind, a in enumerate(ax.flat):
        image_to_eval_fn = unseen_dataset_list[ind]
        image_to_eval = PIL.Image.open(os.path.join(unseen_dataset_dir, image_to_eval_fn)).convert('RGB')
        a.imshow(image_to_eval)

        tensor_input = transform_chain(image_to_eval).unsqueeze(0).to(device)

        outputs = model(tensor_input)
        _, predicted = torch.max(outputs.data, 1)

        a.set_title(class_labels[predicted])
        a.axis('off')
    plt.tight_layout()
    if save_prediction_image_name is not None:
        plt.savefig(save_prediction_image_name, dpi=200)
    plt.show()

def eval_on_image(
    image_path,
    model,
    transform_chain,
    class_labels,
    device,
    save_prediction_image_name="single_image_eva;.png",
    cascade_file="lbpcascade_animeface.xml",
    expand_factor=20,
    cascade_scale_factor=1.01,
    cascade_min_neighbors=6
    ): 
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    
    cascade = cv.CascadeClassifier(cascade_file)
    image = cv.imread(image_path, cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = cascade_scale_factor,
                                     minNeighbors = cascade_min_neighbors,
                                     minSize = (24, 24))
    if len(faces) == 0:
        return []
    else:
        faces = faces.reshape(-1)
    
    image = PIL.Image.open(image_path)
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.axis("off")
    # note, faces array is returned in convention (x_upper_left, y_upper_left, width, height)
    # need to modify to fit with PIL convention of (left, upper, right, lower)

    # loop through each face, and add to a list
    face_coordinate_list = []

    for i in range(len(faces)//4):
        face_coordinate_list.append(
            (
                faces[i*4+0]-expand_factor, 
                faces[i*4+1]-expand_factor, 
                faces[i*4+2]+expand_factor, 
                faces[i*4+3]+expand_factor
            )
        )
    model.eval()
    for face_coor in face_coordinate_list:
        x, y, wx, wy = face_coor
        # print(x, y, x+wx, y+wy)
        # cropping out image for CNN classificaiton
        test_crop = resize_image_to_square(image.crop((x, y, x+wx, y+wy)))
        tensor_input = transform_chain(test_crop).unsqueeze(0).to(device)
        outputs = model(tensor_input)
        _, predicted = torch.max(outputs.data, 1)
        # print(_, predicted)
        predicted_class = class_labels[predicted]

        rect = patches.Rectangle((x, y), wx, wy, linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        ax.text(
            x+20, y-10, predicted_class, ha="center", va="center", size=5,
            bbox=dict(boxstyle="square", fc="pink", ec="b", lw=0)
            )
    if save_prediction_image_name is not None:
        plt.savefig(save_prediction_image_name, dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()
    
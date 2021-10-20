import torch
import matplotlib.pyplot as plt
import os
import PIL

def eval_on_folder(
    dataset, 
    model, 
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
    class_labels = dataset.classes
    transform_chain = dataset.transform

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
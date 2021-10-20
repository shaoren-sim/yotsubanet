import os
from webscraper.utils import count_data_in_folder, preview_data_folder

DATA_FOLDER = "data"
labels = os.listdir(DATA_FOLDER)
print(labels)

for label in labels:
    image_counts = count_data_in_folder(os.path.join(DATA_FOLDER, label))
    print(f"{label}: {image_counts} images.")

for label in labels:
    print("Plotting", label)
    preview_data_folder(os.path.join(DATA_FOLDER, label), f"Label: {label}")
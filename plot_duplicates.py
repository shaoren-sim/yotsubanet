# %%
from dataset_cleanup.image_duplicate_detection import DuplicateDetection

DATA_DIR = "/home/shaoren/Desktop/yotsubanet/data"

dupe_detect = DuplicateDetection(
    DATA_DIR,
    "/home/shaoren/Desktop/yotsubanet/extra_unlabelled_data/multiple_faces",
)

dupe_detect.count_images()
dupe_detect.inspect_duplicates()
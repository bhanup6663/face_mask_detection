import os
import random
import shutil

# Function to create directory if not exists
def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Source directories
images_dir = '/Users/bhanuprakash/Documents/trainings/Yolo/archive/images'  
annotations_dir = '/Users/bhanuprakash/Documents/trainings/Yolo/annotations' 

# Destination directories
base_output_dir = 'new_dataset'
images_output_dir = os.path.join(base_output_dir, 'images')
labels_output_dir = os.path.join(base_output_dir, 'labels')

# Create necessary directories
create_dir_if_not_exists(base_output_dir)
create_dir_if_not_exists(images_output_dir)
create_dir_if_not_exists(labels_output_dir)

# Subdirectories for train, test, and val
for subset in ['train', 'test', 'val']:
    create_dir_if_not_exists(os.path.join(images_output_dir, subset))
    create_dir_if_not_exists(os.path.join(labels_output_dir, subset))

# List all images
image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]

# Split into train, test, val
random.shuffle(image_files)
num_images = len(image_files)
train_split = int(0.7 * num_images)
test_split = int(0.2 * num_images)
val_split = num_images - train_split - test_split

train_images = image_files[:train_split]
test_images = image_files[train_split:train_split + test_split]
val_images = image_files[train_split + test_split:]

# Function to copy files to destination folder
def copy_files(file_list, src_img_dir, src_ann_dir, dest_img_dir, dest_ann_dir):
    for file_name in file_list:
        # Copy images
        shutil.copy(os.path.join(src_img_dir, file_name), os.path.join(dest_img_dir, file_name))
        
        # Find corresponding annotation file
        annotation_file = os.path.splitext(file_name)[0] + '.txt'
        shutil.copy(os.path.join(src_ann_dir, annotation_file), os.path.join(dest_ann_dir, annotation_file))

# Copy images and annotations to respective directories
copy_files(train_images, images_dir, annotations_dir, os.path.join(images_output_dir, 'train'), os.path.join(labels_output_dir, 'train'))
copy_files(test_images, images_dir, annotations_dir, os.path.join(images_output_dir, 'test'), os.path.join(labels_output_dir, 'test'))
copy_files(val_images, images_dir, annotations_dir, os.path.join(images_output_dir, 'val'), os.path.join(labels_output_dir, 'val'))

print("Dataset split and copied successfully.")

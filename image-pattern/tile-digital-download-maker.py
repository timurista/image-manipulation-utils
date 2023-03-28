import os
import shutil
import zipfile

from dotenv import load_dotenv

load_dotenv()


def create_folder_with_images(input_folder, output_folder, num_images):
    # Create the output folder
    os.makedirs(output_folder, exist_ok=True)

    # Move the specified number of images to the output folder
    moved_images = 0
    for filename in os.listdir(input_folder):
        if moved_images >= num_images:
            break

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Check if the file is an image
        if not os.path.isfile(input_path) or not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # copy the image to the output folder
        shutil.copy(input_path, output_path)
        moved_images += 1

    # Create a zip file for the output folder
    with zipfile.ZipFile(f"{output_folder}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_folder))

def process_images(input_folder, outfolder):
    # Count the number of image files in the input folder
    num_images = sum(1 for filename in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, filename)) and filename.lower().endswith(('.png', '.jpg', '.jpeg')))

    # Check if there are at least 50 images in the input folder
    if num_images < 50:
        raise ValueError("The input folder must contain at least 50 images. The current folder contains " + str(num_images) + " images.")

    folder1 = os.path.join(outfolder, "output_10_images")
    folder2 = os.path.join(outfolder, "output_20_images")
    folder3 = os.path.join(outfolder, "output_50_images")

    # Create the three output folders and fill them with images
    create_folder_with_images(input_folder, folder1, 10)
    create_folder_with_images(input_folder, folder2, 20)
    create_folder_with_images(input_folder, folder3, 50)

    print("Done")

# Set your input folder path
input_folder = os.getenv('INPUT_DIR')
outfolder = os.getenv('OUT_FOLDER_DIR')

# Process the images
process_images(input_folder, outfolder)

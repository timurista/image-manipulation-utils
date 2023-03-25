import os

# import dotenv to load the directory for in/ out
from dotenv import load_dotenv
from PIL import Image

load_dotenv()



def tile_image(input_path, output_path, new_size):
    # Open the input image
    img = Image.open(input_path)

    # Calculate how many times the pattern needs to be repeated
    num_x = new_size // img.width + 1
    num_y = new_size // img.height + 1

    # Create a new blank image with the desired size
    tiled_img = Image.new("RGB", (new_size, new_size))

    # Tile the input image onto the blank image
    for i in range(num_x):
        for j in range(num_y):
            tiled_img.paste(img, (i * img.width, j * img.height))

    # Save the tiled image to the output path
    tiled_img.save(output_path)

def process_images(input_dir, output_dir, new_size=1920):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all the files in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if the file is an image
        if not os.path.isfile(input_path) or not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Tile and save the image
        tile_image(input_path, output_path, new_size)

# Set your input and output directories
input_dir = os.getenv('INPUT_DIR')
output_dir =  os.getenv('OUTPUT_DIR')
new_size = int(os.getenv('NEW_SIZE'), 1920)

# Process the images
process_images(input_dir, output_dir, new_size)

print("Done!")

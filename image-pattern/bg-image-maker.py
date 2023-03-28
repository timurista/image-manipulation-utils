import argparse
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont

total_width = 2000
total_height = 1200

def crop_center(img, crop_width, crop_height):
    img_width, img_height = img.size
    left = (img_width - crop_width) / 2
    top = (img_height - crop_height) / 2
    right = (img_width + crop_width) / 2
    bottom = (img_height + crop_height) / 2
    return img.crop((left, top, right, bottom))

def create_bg_image(bg_dir, num_images, output_path, title, tagline, title_font, title_color, tagline_font, tagline_color):
    # Get the image paths from the background directory
    image_paths = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Open the images and store them in a list
    images = [Image.open(path) for path in image_paths[:num_images]]

    # Calculate the width and height of each column
    output_width = total_width
    output_height = total_height
    column_width = output_width // num_images

    # Crop the images from the center to fit the column dimensions
    cropped_images = [crop_center(img, column_width, output_height) for img in images]

    # Create a new image with the output dimensions
    bg_image = Image.new('RGB', (output_width, output_height), color='white')

    # Paste the cropped images in vertical columns
    x_offset = 0
    for img in cropped_images:
        bg_image.paste(img, (x_offset, 0))
        x_offset += img.width

    # Check if the last column has remaining width
    remaining_width = output_width - x_offset
    if remaining_width > 0:
        # Add one more image to fill the remaining width
        extra_img = crop_center(images[-1], remaining_width, output_height)
        bg_image.paste(extra_img, (x_offset, 0))

    # Draw the divider rectangle
    divider_height = int(output_height * 0.125)
    divider_width = int(output_width * 1)
    divider_color = "#E5E7EB"  # Bluish-greyish color
    divider_x = (output_width - divider_width) // 2
    divider_y = (output_height - divider_height) // 2
    divider_rect = Image.new('RGB', (divider_width, divider_height), color=divider_color)
    bg_image.paste(divider_rect, (divider_x, divider_y))


    # Create a white rectangle in the center of the image
    rect_width = int(output_width * 0.7)
    rect_height = int(output_height * 0.4)
    rect_x = (output_width - rect_width) // 2
    rect_y = (output_height - rect_height) // 2
    rectangle = Image.new('RGB', (rect_width, rect_height), color='white')
    bg_image.paste(rectangle, (rect_x, rect_y))

     # Draw a drop shadow for the white rectangle
    shadow_color = "black"
    shadow_offset = (5, 5)
    shadow_blur_radius = 10
    shadow_image = Image.new('RGBA', bg_image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_image)
    shadow_draw.rectangle([(rect_x+shadow_offset[0], rect_y+shadow_offset[1]), (rect_x+rect_width+shadow_offset[0], rect_y+rect_height+shadow_offset[1])], fill=shadow_color)
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(shadow_blur_radius))

    # Create an alpha mask for the white rectangle
    mask = Image.new('L', (rect_width, rect_height), color=255)

    # Draw the white rectangle again to make it visible over the shadow
    bg_image.paste(rectangle, (rect_x, rect_y), mask=mask)


    # Draw the title and tagline in the center of the rectangle
    draw = ImageDraw.Draw(bg_image)

    title_font_size = int(rect_height * 0.3)
    tagline_font_size = int(rect_height * 0.15)

    if title_font == "":
        title_font = ImageFont.load_default()
    else:
        title_font = ImageFont.truetype(title_font, title_font_size)

    if tagline_font == "":
        tagline_font = ImageFont.load_default()
    else:
        tagline_font = ImageFont.truetype(tagline_font, tagline_font_size)

    title_width, title_height = draw.textbbox((0, 0), title, font=title_font)[2:4]
    title_x = (total_width - title_width) // 2
    title_y = rect_y + (rect_height - title_height - tagline_font_size) // 2

    tagline_width, tagline_height = draw.textbbox((0, 0), tagline, font=tagline_font)[2:4]
    tagline_x = (total_width - tagline_width) // 2
    tagline_y = title_y + title_height

    draw.text((title_x, title_y), title, font=title_font, fill=title_color)
    draw.text((tagline_x, tagline_y), tagline, font=tagline_font, fill=tagline_color)


    # Save the output image
    bg_image.save(output_path)

def main(args):
    create_bg_image(args.bg_dir, args.num_images, args.output, args.title, args.tagline, args.title_font, args.title_color, args.tagline_font, args.tagline_color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a background image with evenly spaced vertical columns of images and custom text.")
    parser.add_argument("bg_dir", help="The directory containing the background images.")
    parser.add_argument("output", help="The path to save the output image.")
    parser.add_argument("title", help="The title to display on the image.")
    parser.add_argument("tagline", help="The tagline to display on the image.")
    parser.add_argument("--num_images", type=int, default=10, help="The number of images to include in the background image. Default: 10")
    parser.add_argument("--title_font", type=str, default="", help="The font file to use for the title. Default: arial.ttf")
    parser.add_argument("--title_color", type=str, default="black", help="The color to use for the title. Default: black")
    parser.add_argument("--tagline_font", type=str, default="", help="The font file to use for the tagline. Default: arial.ttf")
    parser.add_argument("--tagline_color", type=str, default="#8B8771", help="The color to use for the tagline. Default: black")

    args = parser.parse_args()
    main(args)

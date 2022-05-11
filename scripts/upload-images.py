#!/usr/bin/env python3

"""
This script is in charge of processing a glob of images, converting them to the webp format,
resize them to a large-but-not-too-large size, and uploading the result to S3.

"""

import argparse
import subprocess
import logging
import tempfile
import glob

from pathlib import Path
from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pre-process images before an article release",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--images", nargs="+", help="The list of images to process", required=True
    )
    parser.add_argument(
        "--s3-folder",
        help="Name of the s3 directory under which the images will be uploaded",
        required=True,
    )
    parser.add_argument(
        "--output-format",
        help="Format into which the images will be converted",
        default="webp",
    )
    parser.add_argument(
        "--output-width-px",
        help="Width of the converted images",
        default=1200,
    )
    return parser.parse_args()


def convert_to_image_format(image_filepath, output_format, save_to_dir):
    """
    Convert the image located at the provided image path to the provided output format.

    """
    image = Image.open(image_filepath).convert("RGB")
    image_path = Path(image_filepath)
    target_image_path = save_to_dir / image_path.name.replace(
        image_path.suffix, f".{output_format}"
    )
    logging.info(f"Saving {target_image_path.name}")
    image.save(target_image_path, output_format)
    return target_image_path


def resize_image(image_filepath, width_px):
    """Resize the image located at the provided image filepath to the provided width, in px.

    The height will automatically be computed given the width downsize ratio.

    If the provided image width is under the target one, nothing will be done.

    """
    image = Image.open(image_filepath)
    original_width, original_height = image.size
    if original_width <= width_px:
        logging.info(
            f"{image_filepath} width is already under {width_px}px ({original_width}px). Skipping resize."
        )
        return
    height_px = int(round(width_px / original_width * original_height))
    logging.info(f"Resizing {image_filepath.name} to ({width_px}, {height_px})px.")
    image.resize((width_px, height_px))
    image.save(image_filepath, dpi=(72, 72))


def upload_image_to_s3(image_path, s3_directory):
    """Upload the provided image to s3."""
    s3_path = f"s3://balthazar-rouberol-blog/{s3_directory}"
    logging.info(f"Uploading {image_path.name} to {s3_path}")
    cmd = [
        "aws",
        "s3",
        "cp",
        str(image_path),
        f"{s3_path}/{image_path.name}",
        "--acl",
        "public-read",
    ]
    subprocess.run(cmd)


def main():
    args = parse_args()
    temp_dir = Path(tempfile.mkdtemp())
    for image_pattern in args.images:
        images = glob.glob(image_pattern)
        for image in images:
            logging.info(f"Processing {image}")
            original_size = round(
                Path(image).expanduser().absolute().lstat().st_size / (1000 ** 2), 1
            )
            converted_image_filepath = convert_to_image_format(
                image, args.output_format, temp_dir
            )
            resize_image(converted_image_filepath, args.output_width_px)
            new_size = round(
                Path(converted_image_filepath).expanduser().absolute().lstat().st_size
                / (1000 ** 2),
                1,
            )

            logging.info(f"Size reduced from {original_size}MB to {new_size}MB")
            upload_image_to_s3(converted_image_filepath, args.s3_folder)


if __name__ == "__main__":
    main()

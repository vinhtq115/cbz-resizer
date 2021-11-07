import argparse
import cv2
import numpy as np
import os.path
import zipfile
from tqdm.contrib.concurrent import process_map
from pathlib import Path


def resize(img, max_width, max_height):
    """
    Resize image with resolution no bigger than (max_width, max_height) while keeping aspect ratio.
    Reference from https://stackoverflow.com/a/64884087/9921431.
    :param img: Image (OpenCV)
    :param max_width: Maximum width
    :param max_height: Maximum height
    :return: Resized image
    """
    side1 = max_height / img.shape[0]
    side2 = max_width / img.shape[1]
    scale_factor = min(side1, side2)
    new_resolution = (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor))
    new_img = cv2.resize(img, new_resolution, interpolation=cv2.INTER_AREA)
    return new_img


def thread(arg):
    cbz_file, max_width, max_height, output_dir = arg
    cbz_filename = os.path.split(cbz_file)[1]
    cbz_save_path = Path(os.path.join(output_dir, cbz_filename)).with_suffix('.cbz')

    with zipfile.ZipFile(cbz_save_path, 'w') as cbz_save:
        with zipfile.ZipFile(cbz_file, 'r') as cbz:
            file_list = cbz.namelist()
            for image in file_list:
                # Read image and resize
                data = cbz.read(image)
                img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                img = resize(img, max_width, max_height)

                # Save image
                ext = image.split('.')[-1]
                retval, buf = cv2.imencode(f'.{ext}', img)
                cbz_save.writestr(image, buf)


def main(args):
    max_width = args.max_width
    max_height = args.max_height
    output_dir = args.output_dir

    cbz_files = args.file
    arg = [(cbz_file, max_width, max_height, output_dir) for cbz_file in cbz_files]
    process_map(thread, arg, max_workers=12)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize CBZ (keep aspect ratio).')
    parser.add_argument('--max_width', type=int, help='max destination width', required=True)
    parser.add_argument('--max_height', type=int, help='max destination height', required=True)
    parser.add_argument('--output_dir', type=str, help='path to save file(s)', required=True)
    parser.add_argument('file', nargs='+', help='path to file')

    _args = parser.parse_args()
    main(_args)

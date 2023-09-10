import sys, pathlib

from PIL import Image
cur_folder = pathlib.Path(__file__).resolve().parent
sys.path.append(str(cur_folder.parent))

from argparse import ArgumentParser
import tools.color_processing as cp
from tools import get_original_files, hue_rotate, invert_color, rgb_to_hsv

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--fast", action="store_false", help="significantly faster processing by skiping compression step")
    parser.add_argument("-i", "--input", help="specify to only process listed file")
    return parser.parse_args()

args = get_args()

def processing(color):
    h, s, _ = rgb_to_hsv(color)
    if abs(h - 39.4) > 5 or s > 60:
        return color
    return hue_rotate(color, 236.9)

def process(in_f: pathlib.Path):
    print(f"Processing {in_f.stem}")
    out_f = cur_folder / in_f.name

    mask = None
    if (f := (cur_folder / "_masks" / in_f.name)).is_file():
        mask = Image.open(f)

    cp.file_process_color(in_f, out_f, processing, args.fast, custom_mask=mask)

if args.input is None:
    for in_f in get_original_files():
        process(in_f)
else:
    process(pathlib.Path(args.input))


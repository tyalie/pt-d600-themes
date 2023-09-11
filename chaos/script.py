"""
My custom theme

Does a simple hue rotate to change the accent color
and has a few nice masks.
"""
import sys, pathlib

from PIL import Image
cur_folder = pathlib.Path(__file__).resolve().parent
sys.path.append(str(cur_folder.parent))

import tools.color_processing as cp
from tools import get_argparse, get_original_files, hue_rotate, rgb_to_hsv

args = get_argparse().parse_args()

def processing(color):
    """
    Rotate all colors with hue between 34.4-44.4°
    and a saturation lower 60% by 236.9°

    in other words: Map orange to lavendel
    """
    h, s, _ = rgb_to_hsv(color)
    if abs(h - 39.4) > 5 or s > 60:
        return color
    return hue_rotate(color, 236.9)

def process(in_f: pathlib.Path):
    print(f"Processing {in_f.stem}")
    out_f = cur_folder / in_f.name

    mask = None
    # I've my own masks in ./_masks. So use these too
    if (f := (cur_folder / "_masks" / in_f.name)).is_file():
        mask = Image.open(f)

    cp.file_process_color(in_f, out_f, processing, args.fast, custom_mask=mask)

if args.input is None:
    for in_f in get_original_files():
        process(in_f)
else:
    process(pathlib.Path(args.input))


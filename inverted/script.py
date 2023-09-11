"""
Simple inverted theme, which preserves the hue of the colors.
"""
import sys, pathlib
cur_folder = pathlib.Path(__file__).resolve().parent
sys.path.append(str(cur_folder.parent))

import tools.color_processing as cp
from tools import get_argparse, get_original_files, hue_rotate, invert_color

args = get_argparse().parse_args()

def processing(color):
    return hue_rotate(invert_color(color), 180)

def process(in_f: pathlib.Path):
    print(f"Processing {in_f.stem}")
    out_f = cur_folder / in_f.name
    cp.file_process_color(in_f, out_f, processing, args.fast)

if args.input is None:
    for in_f in get_original_files():
        process(in_f)
else:
    process(pathlib.Path(args.input))


import sys, pathlib
cur_folder = pathlib.Path(__file__).resolve().parent
sys.path.append(str(cur_folder.parent))

from argparse import ArgumentParser
import tools.color_processing as cp
from tools import get_original_files, hue_rotate, invert_color

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--fast", action="store_false", help="significantly faster processing by skiping compression step")
    parser.add_argument("-i", "--input", help="specify to only process listed file")
    return parser.parse_args()

args = get_args()

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


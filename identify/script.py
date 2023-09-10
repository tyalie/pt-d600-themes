import sys, pathlib

from PIL import Image, ImageDraw, ImageFont, ImageColor
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

COLOR_CODES = ["red", "lime", "orchid", "green", "fuchsia", "blue", "turquoise"]

def draw_id_pattern(img: Image.Image, id: int):
    txt = Image.new("RGBA", img.size[::-1], (0,0,0,0))

    label = f"{id:03}"
    color = (*ImageColor.getrgb(COLOR_CODES[id % len(COLOR_CODES)]), int(0.8*255))

    d = ImageDraw.Draw(txt)
    bounding_box = d.textbbox((0,0), label)

    t_width = bounding_box[2] - bounding_box[0]
    t_height = bounding_box[3] - bounding_box[1]

    for x in range(0, txt.width, t_width + 5):
        for y in range(0, txt.height, t_height + 2):
            d.text((x,y), f"{id:03}", fill=color, align="center")

    txt = txt.rotate(90, expand=True)

    return Image.alpha_composite(img.convert("RGBA"), txt).convert("RGB")

def process(in_f: pathlib.Path):
    print(f"Processing {in_f.stem}")
    out_f = cur_folder / in_f.name

    img = Image.open(in_f).convert("RGB")

    # apply identifying mask
    # - get id
    i_id =int(in_f.stem[:4])
    img = draw_id_pattern(img, i_id)

    cp.save_optimized_file(img, out_f, args.fast)

if args.input is None:
    for in_f in get_original_files():
        process(in_f)
else:
    process(pathlib.Path(args.input))


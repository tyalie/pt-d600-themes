"""
Debugging theme that can be used to identify components on the UI.

Each image will get a 3-digit number and color combination overlay,
which helps uniquly identifying which image index is used where.

This is really helpful, as there are like at least 3 versions of the
same blank background in the table and each serves a different purpose.

!warning: Don't use it for too long. It's almost painful to look at.
"""
import sys, pathlib

from PIL import Image, ImageDraw, ImageFont, ImageColor
cur_folder = pathlib.Path(__file__).resolve().parent
sys.path.append(str(cur_folder.parent))

import tools.color_processing as cp
from tools import get_argparse, get_original_files

args = get_argparse().parse_args()

COLOR_CODES = ["red", "lime", "orchid", "green", "fuchsia", "blue", "turquoise"]

def draw_id_pattern(img: Image.Image, id: int):
    """
    Draws the identifying pattern on the image.
    The pattern consists of repeating tiles of the three-digit
    table index number and to allow better seperation of elements,
    the code is written using a color choosen by its index and
    the above COLOR_CODES table.
    """
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

    i_id =int(in_f.stem[:4])
    img = draw_id_pattern(img, i_id)

    cp.save_optimized_file(img, out_f, args.fast)

if args.input is None:
    for in_f in get_original_files():
        process(in_f)
else:
    process(pathlib.Path(args.input))


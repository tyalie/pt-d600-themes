from typing import Callable, Tuple, Optional
from pathlib import Path
from PIL import Image
import numpy as np
from subprocess import run
import tempfile
import io

IGNORE_COLOR = (0xff, 0x00, 0xff)
GIMP_CALL = ["flatpak", "run", "org.gimp.GIMP"]
MASK_FOLDER = Path(__file__).resolve().parent / "../_masks"
IMAGE_DPI = (37.8, 37.8)

_COLOR = Tuple[int,int,int]

def apply_mask(img: Image.Image, mask: Image.Image) -> Image.Image:
    """
    Apply a mask using alpha composite. In other words the mask is being
    add to the originam image using the information from the alpha layer.

    @return RGB image
    """
    return Image.alpha_composite(img.convert("RGBA"), mask).convert("RGB")

def apply_mask_from_dir(img: Image.Image, name: str) -> Image.Image:
    """
    Apply a mask from the common "_masks" directory in the root
    of the project. Provided a file name has been given, the mask
    gets choosen automatically.
    """
    mask_file = MASK_FOLDER / name
    if not mask_file.is_file():
        return img

    mask = Image.open(mask_file)
    return apply_mask(img, mask)

def process_color(img: Image.Image, func: Callable[[_COLOR], _COLOR]) -> Image.Image:
    """
    Applies a mapping function from one color to another,
    on the given image.

    Note here, that the mapping function will only be called once
    per color. Additionally the 'magic ping' chroma key (#ff00ff)
    cannot be remapped as it encodes 1-bit transparency.
    """
    data = np.array(img)
    n_data = data.copy()

    for color in np.unique(data.reshape((-1,3)), axis=0):
        # ignore color used for masking
        if tuple(color) == IGNORE_COLOR:
            continue
        n_data[(data == color).all(axis = -1)] = np.array(func(color))

    return Image.fromarray(n_data, mode="RGB")

def _do_im_processing(b: bytes) -> bytes:
    """
    Use gimp to compress bmp file as pillow doesn't
    support RLE compression for storage. Additionally
    make sure that we're BMP3 compliant.

    !requires GIMP >v2.10.30 but below v2.99 for
    file-bmp-save2 cmd

    on the choice of GIMP:
        I've tried quite a few things to get the image
        size as small as possible. As we're heavily
        restricted by the available flash, it's an
        important metric to optimize for.

        Sadly the obvious choice of imagemagick doesn't
        work here as their bmp files are anything but
        optimized towards size.
    """

    with tempfile.TemporaryDirectory() as folder:
        in_file = folder + "/in.bmp"
        out_file = folder + "/out.bmp"

        batch_script = f"""
        (let*
          (
            (i (car (file-bmp-load 1 "{in_file}" "-")))
            (d (car (gimp-image-get-active-drawable i)))
          )
          (file-bmp-save2 1 i d "{out_file}" "" 1 1 3)
        )
        """

        with open(in_file, "wb") as fp:
            fp.write(b)

        proc = run(
            [
                *GIMP_CALL,         # our gimp executable
                "-i",               # don't run in interactive mode
                "-d", "-f", "-s",   # don't load brushed, data & co
                "-b", batch_script, # first batch command
                "-b", "(gimp-quit 0)"
            ],
            capture_output=True
        )
        if proc.returncode != 0:
            print(f"GIMP failed to execute")
            print(f"- Return code: {proc.returncode}")
            print(f"- stderr: {proc.stderr}")
            raise Exception("GIMP error")

        with open(out_file, "rb") as fp:
            return fp.read()

def _img_to_bytes(img: Image.Image) -> bytes:
    """
    Convert image into a bytes object
    """
    # store in bytes
    b = io.BytesIO()
    img.info["dpi"] = IMAGE_DPI
    img.save(b, filename="", format="bmp")
    return b.getvalue()

def _img_to_bytes_palette(img: Image.Image) -> bytes:
    """
    Convert image into bytes using a palette
    which is automatically generated.
    """
    # set a palette again
    img = img.convert('P', palette=Image.Palette.ADAPTIVE)
    return _img_to_bytes(img)

def _img_to_bytes_direct(img: Image.Image) -> bytes:
    """
    Convert image into bytes using the BMP direct
    mode, without a peltte
    """
    # set direct mode (remove palette if necessary)
    img = img.convert("RGB")
    return _img_to_bytes(img)


def save_optimized_file(img: Image.Image, output: str | Path, compress: bool = True):
    """
    Save a bmp file and choose the smallest possible version (palette
    vs. direct). This is important as the bitmaps need to fit into the
    storage space.

    @param compress If True, compress image using the compression pipeline.
                    This can take a lot longer.
    """
    # generate with and without palette to see which is smaller
    b_palette = _img_to_bytes_palette(img)
    b_direct = _img_to_bytes_direct(img)

    # choose smallest
    data = b_palette if len(b_palette) < len(b_direct) else b_direct
    if compress:
        data = _do_im_processing(data)

    print(f"Writing {len(data)} bytes (palette < direct: {len(b_palette) < len(b_direct)})")
    with open(output, "wb") as fp:
        fp.write(data)

def file_process_color(in_file: str | Path, output: str | Path, func: Callable[[_COLOR], _COLOR], compress: bool = True, do_masking: bool = True, custom_mask: Optional[Image.Image] = None):
    """
    Process an image file with the specified masks, color remappings, …
    and store it in the specified location.

    Note here that the custom_mask is applied before the general
    masks in _masks

    @param in_file input file name
    @param output output file name
    @param func Color mapping function
    @param compress If true, compresses image. This is not fast
    @param do_masking If true uses the masks in _masks to preserve important UI elements
    @param custom_mask if provided, will apply a custom user mask to the image
    """
    img = Image.open(in_file).convert("RGB")

    img = process_color(img, func)

    if custom_mask is not None:
        img = apply_mask(img, custom_mask)

    if do_masking:
        img = apply_mask_from_dir(img, Path(in_file).name)

    save_optimized_file(img, output, compress)

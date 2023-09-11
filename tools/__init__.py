from .original import get_original_files
from .color_processing import _COLOR
from typing import Tuple
from argparse import ArgumentParser
import colorsys

def _color_int_to_float(color: _COLOR) -> Tuple[float,float,float]:
    return tuple(map(lambda v: v/0xff, color))

def _color_float_to_int(color: Tuple[float,float,float]) -> _COLOR:
    return tuple(map(lambda v: int(v*0xff), color))

def rgb_to_hsv(color: _COLOR) -> Tuple[float, float, float]:
    """
    Convert an RGB to a HSV color.

    The domain of each channel is:
        ([0-360], [0-100], [0-100])
    """
    h, s, v =  colorsys.rgb_to_hsv(*_color_int_to_float(color))
    return h * 360, s * 100, v * 100

def hue_rotate(color: _COLOR, angle_deg: float) -> _COLOR:
    """
    Rotate hue of color by an angle.

    @param color Color with channel in range 0-255
    @param angle_deg Angle in degrees [0-360] to rotate hue with
    """
    v = list(colorsys.rgb_to_hsv(*_color_int_to_float(color)))
    v[0] = ((v[0] * 360 + angle_deg) / 360) % 1

    return _color_float_to_int(colorsys.hsv_to_rgb(*v))

def invert_color(color: _COLOR) -> _COLOR:
    """
    Invert color. Note that each channel is in range 0-255
    """
    return (0xff - color[0], 0xff - color[1], 0xff - color[2])

def get_argparse():
    parser = ArgumentParser()
    parser.add_argument("-f", "--fast", action="store_false", help="significantly faster processing by skiping compression step")
    parser.add_argument("-i", "--input", help="specify to only process listed file")
    return parser


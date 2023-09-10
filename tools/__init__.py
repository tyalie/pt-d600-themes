from .original import get_original_files
from .color_processing import _COLOR
from typing import Tuple
import colorsys

def _color_int_to_float(color: _COLOR) -> Tuple[float,float,float]:
    return tuple(map(lambda v: v/0xff, color))

def _color_float_to_int(color: Tuple[float,float,float]) -> _COLOR:
    return tuple(map(lambda v: int(v*0xff), color))

def rgb_to_hsv(color: _COLOR) -> Tuple[float, float, float]:
    h, s, v =  colorsys.rgb_to_hsv(*_color_int_to_float(color))
    return h * 360, s * 100, v * 100

def hue_rotate(color: _COLOR, angle_deg: float) -> _COLOR:
    v = list(colorsys.rgb_to_hsv(*_color_int_to_float(color)))
    v[0] = ((v[0] * 360 + angle_deg) / 360) % 1

    return _color_float_to_int(colorsys.hsv_to_rgb(*v))

def invert_color(color: _COLOR) -> _COLOR:
    return (0xff - color[0], 0xff - color[1], 0xff - color[2])

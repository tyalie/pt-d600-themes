# PT-D600 Theming repo

This repo contains my own themes for the Brother PT-D600 label printer.
As described in the accompanying repo [Brother PD3 Modifier][1], the COLOR PD3 file
contains all that surrounds the label printers UI elements. And as the protocol has
been reversed, we can now provide our own theming for the little printer.

## Repo structure

```
├── original  # original UI elements from the PT-D600 COLOR PD3 file
│   ├── header.json   # important header file
│   ├── 0001-16x32.bmp
│   ⋮ 
├── identify  # the custom identify theme
│   ├── header.json  
│   ├── script.py     # generator script for this theme
│   ├── 0001-16x32.bmp
│   ⋮
├── other theme
│   ├── header.json
│   ├── script.py
│   ├── …
│   ⋮
├── _masks  # important masks to preserve UI
│   ├── 0001-16x32.bmp
│   ⋮ 
├── requirements.txt  # dependencies
└── tools  # python toolset
    ├── …
    ⋮
```

The special folders here are the `original`, `tools` and `_masks` folder. These
contain the original UI files, the software toolset to generate themes and a
collection of masks which are important to preserve UI integrity in this order.

### A theme

As you can see above each (custom) theme consists of at least two files. A
`header.json` and `script.py`. 

The `header.json` contains important information for the PD3 building process (see
[the modifier repo][1]). If you create a new theme, it's best to copy this over and
leave it mostly untouched.

The other file `script.py` is the more interesting one. Most themes will probably at
least partially automatically generate themselves. This can be done using the
`script.py` and using the provided tools. An example application would be to
automatically be able to adjust the accent color, make a darker theme, … As each
theme contains around 1000 images, this could get quite cumbersome to do by hand.
An additional very important benefit of the `script.py` is its ability to recompress
the images so that they fit into the PT-D600 flash.

## How to use it

### Dependencies

First, install the dependencies from the `requirements.txt`. (It's best to
use a virtual environment for this).

You'll also require GIMP >2.10.30 but smaller than 2.99 for this. ImageMagick isn't
able to compress the images small enough, Pillow doesn't support any compression and
GIMP 2.99 is currently non-stable and has a different calling scheme. (palette
bitmaps work again, I'm happy to change this).

> [!NOTE]
> I've only found these tools so far to process BMPv3 images. If you know
> about anything better, please inform me. I'm happy to throw out awkward the
> dependency to GIMP.

### Building a theme

You can generate a theme by calling `python identify/script.py` in the root folder.
This will automatically generate all the images for the theme. As compression can
take around 30min due to stupid dependencies, there are also a few other common
parameters available

```bash
# generate images without compression. 
python identify/script.py -f

# only generate theming image for 0001-16x32.bmp
python identify/script.py -i ./original/0001-16x32.bmp
```

To read up on how to repackage these, look in the [modifier repo][1]


### Creating a theme

It is recommended to create a theme by copying over an existing `script.py` and
`header.json` file from another theme.

Look into the `script.py` to find out how they are written. Additionally, a few hints

- `chaos`: Contains custom masks
- `invert`: A simple theme which does color inversion
- `identify`: A debug theme which overlays the table index on all images


[1]: https://github.com/tyalie/brother-pd3-modifier

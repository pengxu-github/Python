#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import glob
import os
import sys
import shutil

try:
    from PIL import Image
except ImportError:
    print("This script requires the Python Imaging Library to be installed.")
    sys.exit(1)

"""
python android_tools/wallpaper_thumb.py input source_folder --width 240 --height 240 -o target_folder
"""


def ensure_wallpaper(inputs, thumb=False):
    # ensure inputs
    if not inputs:
        inputs = ['.']
    elif isinstance(inputs, str):
        inputs = [inputs]

    # ensure image files
    files = []
    for i in inputs:
        if os.path.exists(i):
            if os.path.isdir(i):
                for f in os.listdir(i):
                    fn = os.path.join(i, f)
                    if os.path.isfile(fn):
                        files.append(fn)
            else:
                files.append(i)
        else:
            files.extend(glob.glob(i))

    files = [f for f in files if
             os.path.splitext(f)[0].endswith('_small') == thumb and
             os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg', '.png', '.bmp')]

    return files


def scale_wallpaper(ratio, width, height, output, inputs):
    # ensure inputs
    files = ensure_wallpaper(inputs)

    # scale image files
    for f in files:
        im = Image.open(f)
        w, h = im.size
        if width and height:
            w, h = int(width), int(height)
        elif width:
            ratio = float(w) / h
            w = int(width)
            h = int(w / ratio)
        elif height:
            ratio = float(w) / h
            h = int(height)
            w = int(h * ratio)
        elif ratio:
            ratio = float(ratio)
            w = int(w * ratio)
            h = int(h * ratio)

        t = '_small'.join(os.path.splitext(os.path.basename(f)))
        if output:
            t = os.path.join(os.path.isdir(output) and output or os.path.dirname(output), t)

        # print('OUT(%dx%d) : %s' % (w, h, t))
        if (w, h) == im.size:
            shutil.copy(f, t)
        else:
            om = im.resize((w, h), Image.ANTIALIAS)
            om.save(t)


def clean_wallpaper(inputs):
    # ensure inputs
    files = ensure_wallpaper(inputs, True)

    # delete image files
    for f in files:
        os.remove(f)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', '-c', action='store_true')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--ratio', type=float)
    parser.add_argument('-mdpi', dest='ratio', action='store_const', const=.6)
    parser.add_argument('-hdpi', dest='ratio', action='store_const', const=.5)
    parser.add_argument('-xhdpi', dest='ratio', action='store_const', const=.4)
    parser.add_argument('-xxhdpi', dest='ratio', action='store_const', const=.3)
    parser.add_argument('--output', '-o')
    parser.add_argument('input', nargs='*')
    args = parser.parse_args(argv)

    if args.clean:
        clean_wallpaper(args.input)
    else:
        scale_wallpaper(args.ratio, args.width, args.height, args.output, args.input)


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python

import os
import sys
import argparse
from PIL import Image

parser = argparse.ArgumentParser("Facebook animated sticker to image sequence script")
parser.add_argument('width', type=int, help="the animation width")
parser.add_argument('height', type=int, help="the animation height, excluding the last row if it's not complete")
parser.add_argument('remaining', type=int, help="the remaining animation tiles on the last row")
parser.add_argument('-os', "--offset", type=int, help="the sticker offset/croppying factor(?)", default=24)
parser.add_argument('image', help="the input image you want processed")
parser.add_argument('-o', '--output', help="output directory", default="./output/")
parser.add_argument('-ox', '--output_width', type=int, help="custom output width", default=0)
parser.add_argument('-oy', '--output_height', type=int, help="custom output height", default=0)

args = parser.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)


img = Image.open(args.image)

if args.remaining == 0: 
    sticker_height = img.height // args.width
else:
    sticker_height = img.height // (args.height + 1)

sticker_width = img.width // args.width
sticker_offset = args.offset
count = 0

for colIndex, row in enumerate(range(args.height + 1)):
    if row == args.height:
        rows = args.remaining
    else:
        rows = args.height
    for rowIndex in range(rows):
        count += 1
        cropped = img.crop((sticker_offset   + sticker_width  *  rowIndex, # left
                            sticker_offset   + sticker_height *  colIndex, # up
                            (-sticker_offset) + sticker_width  * (rowIndex + 1), # right
                            (-sticker_offset) + sticker_height * (colIndex + 1))) # down

        if args.output_width != 0 and args.output_height != 0:
            cropped.thumbnail((args.output_width, args.output_height))
        cropped.save(args.output + "{:03d}.png".format(count))

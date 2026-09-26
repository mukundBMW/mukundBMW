"""Offline portrait preparation using a hand-traced normalized silhouette.
The supplied mask matches the included portrait crop; change it for another photo.
No model downloads, inference runtimes, telemetry, or network calls are used.
"""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter
ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('photo')
    parser.add_argument('--mask', default=str(ROOT/'data/portrait-mask.json'))
    args = parser.parse_args()
    photo = ImageOps.exif_transpose(Image.open(args.photo)).convert('RGB')
    points = json.loads(Path(args.mask).read_text())['normalized_polygon']
    mask = Image.new('L', photo.size, 0)
    ImageDraw.Draw(mask).polygon([(round(x*photo.width), round(y*photo.height)) for x,y in points],fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(.7))
    gray = cv2.cvtColor(np.array(photo),cv2.COLOR_RGB2GRAY)
    enhanced = cv2.createCLAHE(clipLimit=2.5,tileGridSize=(8,8)).apply(gray)
    result = Image.composite(Image.fromarray(enhanced),Image.new('L',photo.size,255),mask)
    ImageOps.pad(result,(800,800),color=255).save(ROOT/'source-prepped.png')
if __name__ == '__main__': main()

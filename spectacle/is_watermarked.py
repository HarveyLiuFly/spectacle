"""
python is_watermarked.py -i lena_modified.tif -m "What's up?"
"""
import argparse
import Image
import matplotlib
import numpy as np
from detect import is_watermarked

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('image')
  parser.add_argument('-w', '--wavelet', default='db1')
  parser.add_argument('-m', '--message', default='locu')
  args = parser.parse_args()
  im = Image.open(args.image)
  data = np.asarray(im)
  hsv = matplotlib.colors.rgb_to_hsv(np.array(data, dtype=float))
  hs = hsv[:, :, 0:2]
  grayscale_data = hsv[:, :, 2]
  print is_watermarked(grayscale_data, args.message, args.wavelet)

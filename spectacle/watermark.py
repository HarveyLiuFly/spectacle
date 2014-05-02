"""
python watermark.py lena_std.tif --alpha 0.7 --wavelet db6
"""

import argparse
import itertools
import numpy as np
from os import path
from embade import embade
from embade import construct_weight
from transform import transform_picture
from transform import recover_picture
from image import hs_brightness_data
from image import image_from_hs_brightness
from message import string_to_ones


def watermark(grayscale_data, message_string, alpha, wavelet, depth=4):
  """
  given a grayscale data of the pixels of the image and the message,
  imbed the message into the picture.
  """
  all_chunks = transform_picture(grayscale_data, depth, wavelet=wavelet)
  message_bits = string_to_ones(message_string)
  chunks_squared = [[np.square(chunk) for chunk in _list]
                    for _list in all_chunks[:-1]]
  new_0_level_chunks = []
  weight = construct_weight(depth, all_chunks[-1], chunks_squared)
  for theta in (0, 1, 2):
    new_0_level_chunks.append(
        embade(all_chunks[0][theta], theta, alpha, weight, message_bits))

  ## Inverse wavelet transform into an image data
  all_chunks[0] = new_0_level_chunks
  import time
  print 'start recover', time.time()
  modified_data = recover_picture(all_chunks, wavelet=wavelet)
  print 'end recover', time.time()

  return modified_data


def keep_values_in_0_255_range(grayscale_data):
  for i, j in itertools.product(xrange(grayscale_data.shape[0]),
                                xrange(grayscale_data.shape[1])):
    if grayscale_data[i, j] > 255:
      grayscale_data[i, j] = 255
    elif grayscale_data[i, j] < 0:
      grayscale_data[i, j] = 0


def main(args):
  hs_data, grayscale_data = hs_brightness_data(args.in_filename)
  watermarked_data = watermark(grayscale_data, args.message, args.alpha,
                               args.wavelet)
  keep_values_in_0_255_range(watermarked_data)
  modified_img = image_from_hs_brightness(hs_data, watermarked_data)
  modified_img.save(args.out_filename)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('in_filename')
  parser.add_argument('-a', '--alpha', type=float, default=1.)
  parser.add_argument('-o', '--out-filename')
  parser.add_argument('-w', '--wavelet', default='db1')
  parser.add_argument('-m', '--message', default='locu')
  args = parser.parse_args()
  if args.out_filename is None:
    name, ext = path.splitext(path.basename(args.in_filename))
    args.out_filename = ('modified-{name}_w-{wavelet}_a-{alpha}{ext}'
                         .format(name=name,
                                 wavelet=args.wavelet,
                                 alpha=args.alpha,
                                 ext=ext))
  main(args)

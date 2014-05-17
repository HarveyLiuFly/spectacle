import Image
import matplotlib
import numpy as np


def hs_brightness_data(image):
  """
  Returns brightness matrix, and hue, saturation matrix
  MxNx2 matrix, and MxN matrix
  """
  if not isinstance(image, Image.Image):
    image = Image.open(image)
  data = np.asarray(image)
  hsv_data = matplotlib.colors.rgb_to_hsv(np.array(data, dtype=float))
  return hsv_data[:, :, :2], hsv_data[:, :, 2]


def image_from_hs_brightness(hs_data, grayscale_data):
  hsv_data = np.dstack((hs_data, grayscale_data))
  data_uint = np.rint(matplotlib.colors.hsv_to_rgb(hsv_data)).astype(np.uint8)
  return Image.fromarray(data_uint)

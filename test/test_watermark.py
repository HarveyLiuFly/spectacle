import numpy as np
from spectacle.detect import _watermark_scores
from spectacle.detect import is_watermarked
from spectacle.image import hs_brightness_data
from spectacle.watermark import watermark


def test_zero_strength_watermark():
  hs, gray_data = hs_brightness_data('data/lena_std.tif')
  watermarked_data = watermark(gray_data, 'my secret message', 0.0, 'db6')
  np.testing.assert_array_equal(np.rint(watermarked_data), np.rint(gray_data),
                                verbose=True)


def test_detection():
  hs, gray_data = hs_brightness_data('data/lena_std.tif')
  assert is_watermarked(gray_data, 'my secret message', 'db6') == False
  watermarked_data = watermark(gray_data, 'my secret message', 0.01, 'db6')
  print _watermark_scores(watermarked_data, 'my secret message', 'db6')
  assert is_watermarked(watermarked_data, 'my secret message', 'db6')

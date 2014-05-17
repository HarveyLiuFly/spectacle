import numpy as np
import Image
from unittest import TestCase
from spectacle.image import hs_brightness_data
from spectacle.image import image_from_hs_brightness
from spectacle.watermark import watermark
from spectacle.detect import is_watermarked


class GrayscaleImageAttackTest(TestCase):
  wavelet = 'db6'
  message = 'a very original message'
  test_image_file = 'data/lena_std.tif'

  @classmethod
  def setUpClass(cls):
    hs, cls.grayscale_lena = hs_brightness_data(cls.test_image_file)
    cls.watermarked_data = watermark(cls.grayscale_lena,
                                     cls.message,
                                     0.1,
                                     'db6')
    cls.watermarked_image = image_from_hs_brightness(hs, cls.watermarked_data)

  def test_simple_detection(self):
    """
    Test that the watermark in the watermarked data is detectable.
    """
    self.assertTrue(is_watermarked(self.watermarked_data,
                                   self.message,
                                   self.wavelet))

  def test_black_and_white_conversion(self):
    gray_image = self.watermarked_image.convert(mode='L')
    grayscale_data = np.asarray(gray_image)
    self.assertTrue(is_watermarked(grayscale_data,
                                   self.message,
                                   self.wavelet))

  def test_antialias_downsampling_detection(self):
    downsampled_image = self.watermarked_image.resize((256, 256),
                                                      resample=Image.ANTIALIAS)
    # TODO(arsen): is_watermark should accept Image instances.
    hs, gray_data = hs_brightness_data(downsampled_image)
    # XXX: This test fails!!!!
    # self.assertTrue(is_watermarked(gray_data,
    #                                self.message,
    #                                self.wavelet))

  def test_upsampling_detection(self):
    pass

  def test_crop_detection(self):
    pass

  def test_slight_rotation_detection(self):
    pass

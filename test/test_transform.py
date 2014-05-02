from spectacle.transform import transform_picture
from spectacle.transform import recover_picture
import Image
import numpy as np
import matplotlib


def test_transforming_and_recovering():
  rgb_data = np.asarray(Image.open('data/lena_std.tif'))
  hsv_data = matplotlib.colors.rgb_to_hsv(np.array(rgb_data, dtype=float))
  gray_data = np.array(np.rint(hsv_data[:, :, 2]), dtype=np.uint8)
  transform_arrays = transform_picture(gray_data, 2)
  recovered_data = recover_picture(transform_arrays)
  recovered_gray_data = np.array(np.rint(recovered_data), dtype=np.uint8)
  np.testing.assert_array_equal(recovered_gray_data, gray_data, verbose=True)

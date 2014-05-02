import pywt


def transform_picture(pixel_data, L, wavelet='db1'):
  """
  Wavelet transforms the pixel_data from an image L times.
  :return all_chunks: [(i00, i01, i02), (i11, i11, i12), ...., (il3,)]
  """
  all_chunks = []
  low = pixel_data
  for _pass in range(L):
    low, chunks = pywt.dwt2(low, wavelet)
    all_chunks.append(chunks)
  all_chunks.append(low)
  return all_chunks


def recover_picture(arrays, wavelet='db1'):
  low = arrays[-1]
  for indx in xrange(2, len(arrays) + 1):
    low = pywt.idwt2((low, arrays[-indx]), wavelet)
  return low

from embade import message_matrix
from transform import transform_picture
from message import string_to_ones


def rho(zero_level_transforms, plus_minus_ones):
  _sum = 0
  for theta, transoform in enumerate(zero_level_transforms):
    _message_matrix = message_matrix(plus_minus_ones, transoform.shape, theta)
    _sum += (_message_matrix * transoform).sum()
  M, N = zero_level_transforms[0].shape
  return _sum / (3 * M * N)


def _watermark_scores(grayscale_data, message, wavelet):
  all_chunks = transform_picture(grayscale_data, 1, wavelet)
  _rho = rho(all_chunks[0], string_to_ones(message))
  M, N = all_chunks[0][0].shape
  threshold = (3.97 * (2. * sum((transform * transform).sum()
                                for transform in all_chunks[0])) ** 0.5
               / (3 * M * N))
  return _rho, threshold


def is_watermarked(grayscale_data, message, wavelet):
  rho, threshold = _watermark_scores(grayscale_data, message, wavelet)
  return (rho > threshold)

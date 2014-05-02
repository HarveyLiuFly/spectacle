import itertools
import numpy as np
from functools import wraps

SCALING_FACTOR = {
  0: 1.,
  1: 0.32, 2: 0.16, 3: 0.1,
}


def message_matrix(message, shape, theta):
  M, N = shape
  thetaMN = theta * M * N
  _matrix = np.zeros(shape)
  message_length = len(message)
  for i, j in itertools.product(xrange(M), xrange(N)):
    indx = thetaMN + i * N + j
    _matrix[i, j] = message[indx % message_length]
  return _matrix


def cache_results(id_function, archive_dict):
  def decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
      _id = id_function(*args, **kwargs)
      rtn_value = archive_dict.get(_id)
      if rtn_value is None:
        rtn_value = function(*args, **kwargs)
        archive_dict[_id] = rtn_value
      return rtn_value
    return wrapper
  return decorator


def constrcut_x(M, N, message):
  """
  Constructs a mapping from i,j indices to the pseudorandom array
  based on the size of the image
  host image should have dimensions of 2Mx2N, so each of first level
  wavelet transforms will have dimensions MxN
  """
  message_length = len(message)

  def x(theta, i, j):
    indx = theta * M * N + i * N + j
    return message[indx % message_length]

  return x


def embade(array, theta, alpha, weight, message):
  """
  Given an array of wavelet transformation coefficients
  :param array: Wavelet transform coefficients
  :param alpha: strenght of the encoding, float [0,1]
  :param weight: functions to calculate stregth coeff
  :param message: message to be encoded
  :param theta: index indicating which of the transforms is the given array
  """
  import time
  start = time.time()
  new_array = np.copy(array)
  M, N = array.shape
  x = constrcut_x(M, N, message)
  print 'before loop', time.time() - start
  w_time, x_time = 0, 0
  for i, j in itertools.product(xrange(M), xrange(N)):
    _t = time.time()
    _w = weight(theta, i, j)
    w_time += time.time() - _t
    _t = time.time()
    _x = x(theta, i, j)
    x_time += time.time() - _t
    new_array[i, j] += alpha * _w * _x
  print 'embade', time.time() - start
  print 'x_time', x_time
  print 'w_time', w_time
  global noise_time
  global lambda_time
  global activity_time
  print 'noise_time', noise_time
  print 'lambda_time', lambda_time
  print 'activity_time', activity_time
  global first_loop_time
  global second_loop_time
  print '1st', first_loop_time
  print '2nd', second_loop_time
  print '1st 2nd ration', first_loop_time / second_loop_time
  return new_array

noise_time = 0
lambda_time = 0
activity_time = 0

def construct_weight(depth, lowlow, transforms_squared):
  """
  Constrcuts the w
  """
  def w(theta, i, j):
    return 0.5 * quantization(0, theta, i, j, lowlow, transforms_squared, depth)
  return w


def quantization(level, theta, i, j, lowlow, transforms_squared, depth):
  """
  """
  # Theta * Lambda * Xi^.2
  # lowlow = transforms[-1]
  import time
  global noise_time
  global lambda_time
  global activity_time
  _t = time.time()
  _noise = noise_sensitivity(level, theta)
  noise_time += time.time() - _t
  _t = time.time()
  _lambda = big_lambda(level, i, j, lowlow, depth)
  lambda_time += time.time() - _t
  _t = time.time()
  _activity = texture_activity(level, i, j, lowlow, transforms_squared, depth) ** 0.2
  activity_time += time.time() - _t
  return _noise * _lambda * _activity


def noise_sensitivity(level, theta):
  return (1.41 if theta == 1 else 0) * SCALING_FACTOR.get(1, 0)


def big_lambda(*args):
  brightness = local_brightness(*args)
  if brightness < 0.5:
    brightness = 1 - brightness
  return 1 + brightness


def local_brightness(level, i, j, lowlow, depth):
  i_ = int(1 + i / 2 ** (depth - 1 - level)) - 1
  j_ = int(1 + j / 2 ** (depth - 1 - level)) - 1
  return 4. ** -(depth) * lowlow[i_, j_]


first_loop_time = 0
second_loop_time = 0

TEXTURE_RESULTS = {}


def t_id_function(level, i, j, low_low, transforms_squared, *args):
  return (level + 10 * (1000 * i + j) +
          10000 * sum(low_low[5]) +
          100000 * sum(transforms_squared[1][2][6, :]))


@cache_results(t_id_function, TEXTURE_RESULTS)
def texture_activity(level, i, j, lowlow, transforms_squared, depth):
  total = 0
  import time
  global first_loop_time
  global second_loop_time
  _t = time.time()
  for k in range(0, depth - level):  # 0, 1, .., depth - l - 1
    interim_sum = 0
    this_level_trasforms = transforms_squared[k + level]
    for theta, x, y in itertools.product(xrange(3), xrange(2), xrange(2)):
      transform_squared = this_level_trasforms[theta]
      _i = int(y + i * .5 ** k) - 1
      _j = int(x + j * .5 ** k) - 1
     # if _i >= transform.shape[0] or _j >= transform.shape[1]:
     #   print 'continue', 'texture'
     #   continue
     # if np.isnan(transform[_i, _j]):
     #   print transform[_i, _j], _i, _j, k + level, theta
      interim_sum += transform_squared[_i, _j]
    total += (16. ** -k) * interim_sum
  first_loop_time += time.time() - _t
  _t = time.time()

  scaled_i = int(1 + i * .5 ** (depth - 1 - level)) - 1
  scaled_j = int(1 + j * .5 ** (depth - 1 - level)) - 1
  var = local_variance(scaled_i, scaled_j, lowlow)
  second_loop_time += time.time() - _t
  return total * var


VARIANCES = {}


# XXX: Assumes lowlow doesn't change and that j < 1000
@cache_results(lambda i, j, lowlow: 1000 * i + j + 1000000 * sum(lowlow[4, :]),
               VARIANCES)
def local_variance(i, j, lowlow):
  neighbor_values = []
  for x, y in itertools.product(xrange(2), xrange(2)):
    _i = i + x
    _j = j + y
    if _i >= lowlow.shape[0] or _j >= lowlow.shape[1]:
      continue
    neighbor_values.append(lowlow[_i, _j])
  if len(neighbor_values) > 1:
    return np.cov(neighbor_values)
  return 0

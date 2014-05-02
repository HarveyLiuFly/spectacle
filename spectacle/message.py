import bitarray


def string_to_ones(string):
  """
  Converts a string into an array of +/- 1s.
  """
  bit_array = bitarray.bitarray()
  bit_array.fromstring(string)
  return [1 if bit else -1 for bit in bit_array]


def ones_to_string(plus_minus_ones):
  """
  Converts a string of +/- 1s into a string.
  """
  return bitarray.bitarray(bit == 1 for bit in plus_minus_ones).tostring()

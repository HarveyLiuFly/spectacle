from spectacle.message import string_to_ones
from spectacle.message import ones_to_string


def test_message_conversion():
  for test_message in ['spectacle', 'hello world']:
    plus_minus_ones = string_to_ones(test_message)
    out_string = ones_to_string(plus_minus_ones)
    assert out_string == test_message

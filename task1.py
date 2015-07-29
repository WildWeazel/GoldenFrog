import unittest

def reverse_and_case(letters):
  return list(reversed([a.upper() if a in 'AaEeIiOoUu' else a.lower() for a in letters]))

class TestReverseAndCase(unittest.TestCase):
  def test_reverse_and_case(self):
    self.assertEqual(reverse_and_case(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']), list('pOIUytrEwq'))
    self.assertEqual(reverse_and_case('The Quick Brown Fox Jumps Over The Lazy Dog'), list('gOd yzAl Eht rEvO spmUj xOf nwOrb kcIUq Eht'))
    self.assertEqual(reverse_and_case('aBCDeFGHiJKLmNoPQRSTuVWXYZ1234567890_'), list('_0987654321zyxwvUtsrqpOnmlkjIhgfEdcbA'))
    self.assertEqual(reverse_and_case(''), [])

if __name__ == '__main__':
  unittest.main()
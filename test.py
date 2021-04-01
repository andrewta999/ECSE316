import numpy as np 
import unittest
from ft_algorithm import FT_1D, inverse_FT_1D, FT_2D, inverse_FT_2D, FFT_1D, inverse_FFT_1D, FFT_2D, inverse_FFT_2D

# mock data for 1D
img1 = np.random.random(32) # 1D array
img1_test = np.fft.fft(img1) # 1D-FFT on this array

# mock data for 2D
img2 = np.random.rand(16, 16) # 2D array
img2_test = np.fft.fft2(img2)   # 2D-FFT on this array


class Test(unittest.TestCase):

    def test_FT_1D(self):
        res = FT_1D(img1)
        compare = np.allclose(res, img1_test)
        self.assertEqual(compare, True)

    def test_inverse_FT_1D(self):
        res = inverse_FT_1D(img1_test).real 
        compare = np.allclose(res, img1)
        self.assertEqual(compare, True)

    def test_FFT_1D(self):
        res = FFT_1D(img1)
        compare = np.allclose(res, img1_test)
        self.assertEqual(compare, True)

    def test_inverse_FFT_1D(self):
        res = inverse_FT_1D(img1_test).real
        compare = np.allclose(res, img1)
        self.assertEqual(compare, True)

    def test_FT_2D(self):
        res = FT_2D(img2)
        compare = np.allclose(res, img2_test)
        self.assertEqual(compare, True)

    def test_inverse_FT_2D(self):
        res = inverse_FT_2D(img2_test).real
        compare = np.allclose(res, img2)
        self.assertEqual(compare, True)

    def test_FFT_2D(self):
        res = FFT_2D(img2)
        compare = np.allclose(res, img2_test)
        self.assertEqual(compare, True)
         
    def test_inverse_FFT_2D(self):
        res = inverse_FFT_2D(img2_test).real
        compare = np.allclose(res, img2)
        self.assertEqual(compare, True)        


unittest.main()


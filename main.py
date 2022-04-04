from KlebLib import fraction, polynomial, rounding, baseconversion, universaladdition
from KlebLib.test import Test
        
if __name__ == '__main__':
    polynomial1 = polynomial.Polynomial('3x^2')
    print(polynomial1.differentiate('x').integrate())
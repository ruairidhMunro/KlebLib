from KlebLib import fraction, polynomial, rounding, baseconversion, universaladdition, series
from KlebLib.test import Test
        
if __name__ == '__main__':
    series1 = series.Series((1, 2, 3), int)
    series1.insert(1, 5)
    print(series1)
from KlebLib import fraction, polynomial, rounding, baseconversion, universaladdition, series
from KlebLib.test import Test
        
if __name__ == '__main__':
    series1 = series.Series([1, 2, 3], int)
    series2 = 0 + series1
    print(list(series2))
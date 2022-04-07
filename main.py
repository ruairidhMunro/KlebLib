from KlebLib import fraction, polynomial, rounding, baseconversion, universaladdition, series
from KlebLib.test import Test
        
if __name__ == '__main__':
    series1 = series.Series(
        [
            series.Series(
                [
                    series.Series([1, 2], int),
                    series.Series([3, 4], int)
                ],
                series.Series,
                int
            ),
            series.Series(
                [
                    series.Series([5, 6], int),
                    series.Series([7, 8], int)
                ],
                series.Series,
                int
            ),
            series.Series(
                [
                    series.Series([9, 10], int),
                    series.Series([11, 12], int)
                ],
                series.Series,
                int
            )
        ],
        series.Series,
        series.Series
    )
    
    print(repr(series1))
#By Caleb Robson
import KlebLib.fraction as fraction
import KlebLib.polynomial as polynomial
import KlebLib.rounding as rounding
import KlebLib.universaladdition as universaladdition 
import KlebLib.baseconversion as baseconversion 

class Test:
    def __init__(self, testType, **kwargs):
        self.testType = testType
        self.kwargs = kwargs

    def test(self, *args):
        if self.testType == 'fraction':
            return self.fractionTest(args)
        elif self.testType == 'polynomial':
            return self.polynomialTest(args)
        elif self.testType == 'baseConversion':
            return self.conversionTest(args)
        elif self.testType == 'universalAddition':
            return self.universalAdditionTest(args)

    def outputVars(self):
        return {'testType': self.testType, 'kwargs': self.kwargs}

    #Individual tests

    def fractionTest(self, args):
        fraction1 = fraction.Fraction(self.kwargs['fraction1'])
        fraction2 = fraction.Fraction(self.kwargs['fraction2'])

        opType = self.kwargs['opType']
        if opType == 'add':
            fraction3 = fraction1 + fraction2
        elif opType == 'subtract':
            fraction3 = fraction1 - fraction2
        elif opType == 'multiply':
            fraction3 = fraction1 * fraction2
        elif opType == 'divide':
            fraction3 = fraction1 / fraction2

        return fraction3.output()

    def polynomialTest(self, args):
        testPolynomial = polynomial.Polynomial(self.kwargs['polynomial'])

        differentiated = testPolynomial.differentiate(args[0])
        integrated = testPolynomial.integrate(args[0])

        return {
            'polynomial': testPolynomial.polynomial,
            'readable': str(testPolynomial),
            'differentiated': differentiated.polynomial,
            'integrated': integrated.polynomial
        }

    def conversionTest(self, args):
        num = self.kwargs['num']
        base = self.kwargs['base']
        convertedBase = self.kwargs['baseToConvertTo']

        return baseconversion.convertBase(num, base, convertedBase)

    def universalAdditionTest(self, args):
        num1 = self.kwargs['num1']
        num2 = self.kwargs['num2']
        base = self.kwargs['base']

        return universaladdition.addNums(base, num1, num2)
        
if __name__ == '__main__':
    test1 = Test(testType='polynomial', polynomial='x^2 - 3x + 4y - 12')
    print(test1.test('x'))
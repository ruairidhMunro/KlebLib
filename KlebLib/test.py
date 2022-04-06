class Test:
    def __init__(self, testType:str, **kwargs):
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

    @property
    def variables(self):
        return {'testType': self.testType, 'kwargs': self.kwargs}

    #Individual tests

    def _fractionTest(self, args):
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

        return str(fraction3)

    def _polynomial_test(self, args):
        testPolynomial = polynomial.Polynomial(self.kwargs['polynomial'])

        differentiated = testPolynomial.differentiate(args[0])
        integrated = testPolynomial.integrate(args[0])

        return {
            'polynomial': testPolynomial.polynomial,
            'readable': str(testPolynomial),
            'differentiated': differentiated.polynomial,
            'integrated': integrated.polynomial
        }

    def _conversion_test(self, args):
        num = self.kwargs['num']
        base = self.kwargs['base']
        convertedBase = self.kwargs['baseToConvertTo']

        return baseconversion.convert_base(num, base, convertedBase)

    def _universal_addition_test(self, args):
        num1 = self.kwargs['num1']
        num2 = self.kwargs['num2']
        base = self.kwargs['base']

        return universaladdition.add(base, num1, num2)
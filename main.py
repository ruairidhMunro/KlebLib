#By Caleb Robson
import fraction
import polynomial
import rounding

class Test:
    def __init__(self, testType, **kwargs):
        self.testType = testType
        self.kwargs = kwargs

    def test(self, *args):
        if self.testType == 'fraction':
            return self.fractionTest(args)
        elif self.testType == 'polynomial':
            return self.polynomialTest(args)

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
        testPolynomial = polynomial.Polynomial(self.kwargs['polynomial'], dictInput=self.kwargs['dictInput'])

        differentiated = testPolynomial.differentiate()
        integrated = testPolynomial.integrate()

        return {
            'polynomial': testPolynomial.output(),
            'differentiated': differentiated.output(),
            'integrated': integrated.output()
        }
        
        
if __name__ == '__main__':
    test1 = Test('fraction', opType='multiply', fraction1='3/4', fraction2='5/6')
    print(test1.test())
    print(test1.outputVars())
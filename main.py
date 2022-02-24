#By Caleb Robson
import re

class Fraction:
    def __init__(self, fraction, listInput=False):
        if listInput:
            self.num = fraction[0]
            self.dem = fraction[1]
        else:
            fraction_nums = fraction.split('/')
            map_object = map(int, fraction_nums)
            fraction_nums = list(map_object)
            self.num = fraction_nums[0]
            self.dem = fraction_nums[1]

        simplified = [x / self.GCD() for x in [self.num, self.dem]]
        if [self.num, self.dem] != simplified:
            self.num = simplified[0]
            self.dem = simplified[1]

    #Get the greatest common divisor of the numerator and denominator
    def GCD(self):
        num1 = self.num
        num2 = self.dem

        if num1 < num2:
            temp = num1
            num1 = num2
            num2 = temp

        remainder = num1 % num2
        while remainder != 0:
            num1 = num2
            num2 = remainder

            remainder = num1 % num2

        return num2

    #Simplify the fraction
    def simplify(self):
        GCD = self.GCD()

        self.num = int(self.num / GCD)
        self.dem = int(self.dem / GCD)

    #Automatically simplify fractions
    def autoSimplify(func):
        def inner(*args, **kwargs):
            fraction = func(*args, **kwargs)
            fraction.simplify
            return fraction

        return inner

    #Output the numbers as a fraction
    def output(self):
        return (f'{self.num}/{self.dem}')

    #Output the fraction as a float
    def outputFloat(self):
        return self.num / self.dem

    #Adds another fraction to this one
    @autoSimplify
    def addFraction(self, fraction2):
        num = (self.num * fraction2.dem) + (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Subtracts another fraction from this one
    @autoSimplify
    def subFraction(self, fraction2):
        num = (self.num * fraction2.dem) - (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Multiplies this fraction by another one
    @autoSimplify
    def timesFraction(self, fraction2):
        num = self.num * fraction2.num
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Divides this fraction by another one
    @autoSimplify
    def divFraction(self, fraction2):
        num = self.num * fraction2.dem
        dem = self.dem * fraction2.num

        return Fraction([num, dem], True)

    #Returns a mixed fraction
    @property
    def mixed(self):
        integerPart = 0
        num = self.num
        dem = self.dem

        while num > dem:
            num -= dem
            integerPart += 1

        return [integerPart, [num, dem]]

    @mixed.setter
    def mixed(self, fraction):
        fraction[1][0] += fraction[0] * fraction[1][1]
        self.num = fraction[1][0]
        self.dem = fraction[1][1]

    #return a list of the numerator and denominator
    def nums(self):
        return ([self.num, self.dem])
        

class Polynomial:
    def __init__(self, polynomial, dictInput=False):
        if dictInput:
            self.polynomial = polynomial
        else:
            self.polynomial = self.parse(polynomial)

    def parse(self, polynomial):
        #print(f'parsing polynomial {polynomial}') #debug
        negatives = []
        additions = re.finditer('[\+-]', polynomial)
        startNegative = re.search('^[\+-]', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negatives.append(i)
                else:
                    negatives.append(i + 1)

        terms = re.split('[\+-]', polynomial)
        if startNegative:
            #print('removed first term') # debug
            del terms[0]

        polynomial = {}
        for i, term in enumerate(terms):
            terms[i] = term.strip()
            term = terms[i]
            #print(f'parsing term {term}') #debug

            #Check if term should be negative
            if i in negatives:
                negativeMultiple = -1
            else:
                negativeMultiple = 1

            if 'x' in term:
                if '^' in term:
                    term = term.split('x^')
                    try:
                        polynomial[float(
                            term[1])] = float(term[0]) * negativeMultiple
                    except ValueError:
                        polynomial[float(term[1])] = negativeMultiple
                else:
                    term = term[:-1]
                    polynomial[1] = float(term) * negativeMultiple
            else:
                polynomial[0] = float(term) * negativeMultiple

        return polynomial

    @property
    def differentiated(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            if coefficient * exponent != 0:  #If the coefficient will not be 0
                polynomial[exponent - 1] = coefficient * exponent

        return polynomial

    @differentiated.setter
    def differentiated(self, polynomial):
        self.polynomial = Polynomial(polynomial, dictInput=True).integrated

    @property
    def integrated(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            polynomial[exponent + 1] = coefficient / (exponent + 1)

        return polynomial

    @integrated.setter
    def integrated(self, polynomial):
        self.polynomial = Polynomial(polynomial, dictInput=True).differentiated

    '''Not doing this
    @property
    def roots(self):
        roots = []
        
        return roots

    @property
    def turningPoints(self):
        turningPoints = []
        
        return turningPoints
    '''

    def output(self, readable=False):
        if readable:
            #TODO output in readable format
            pass
        else:
            return self.polynomial
            

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
        fraction1 = Fraction(self.kwargs['fraction1'])
        fraction2 = Fraction(self.kwargs['fraction2'])

        opType = self.kwargs['opType']
        if opType == 'add':
            fraction3 = fraction1.addFraction(fraction2)
        elif opType == 'subtract':
            fraction3 = fraction1.subFraction(fraction2)
        elif opType == 'multiply':
            fraction3 = fraction1.timesFraction(fraction2)
        elif opType == 'divide':
            fraction3 = fraction1.divFraction(fraction2)

        return fraction3.output()

    def polynomialTest(self, args):
        polynomial = Polynomial(self.kwargs['polynomial'],
                                dictInput=self.kwargs['dictInput'])

        differentiated = Polynomial(polynomial.differentiated, dictInput=True)
        integrated = Polynomial(polynomial.integrated, dictInput=True)

        return {
            'polynomial': polynomial.output(),
            'differentiated': differentiated.output(),
            'integrated': integrated.output()
        }
        

def ceiling(num, decPlaces=0):
    #Set up variables
    overflow = False
    num = str(num)
    numDigits = []
    for digit in num:
        numDigits.append(digit)
    decPoint = numDigits.index('.')

    #Removes the decimal point and finds the last decimal place that will remain
    del numDigits[decPoint]
    lastPlace = decPoint + decPlaces - 1

    #Turns all of the digits into int
    for i, digit in enumerate(numDigits):
        numDigits[i] = int(digit)

    #Rounds up
    complete = False
    roundMod = 0
    while not complete:
        if numDigits[lastPlace - roundMod] < 9:
            #If 1 can be added to the selected position
            numDigits[lastPlace - roundMod] += 1
            complete = True
        else:
            if numDigits[lastPlace] - roundMod - 1 < 0:
                numDigits.insert(0, 1)
                complete = True
                overflow = True
            else:
                numDigits[lastPlace - roundMod] = 0
                roundMod += 1

    #Remove the extra digits
    while len(numDigits) > lastPlace + 1:
        del numDigits[-1]

    #Reformats and outputs the answer
    numDigits.insert(decPoint + int(overflow), '.')
    num = ''
    for i in numDigits:
        num += str(i)
    num = float(num)
    return num
    
def smartRound(num, decPlaces):
    if str(num)[decPlaces + 1] >= 5:
        return ceiling(num)
    else:
        return round(num, 0)
        
        
if __name__ == '__main__':
    test1 = Test('polynomial', polynomial='x^3 - 2x + 5', dictInput=False)
    print(test1.test())
    #print(test1.outputVars())
import re

class Fraction:
    def __init__(self, fraction, listInput=False):
        if isinstance(fraction, list):
            self.num = fraction[0]
            self.dem = fraction[1]
            
        elif isinstance(fraction, str):
            fractionNums = fraction.split('/')
            fractionNums = [int(i) for i in fractionNums]
            self.num = fractionNums[0]
            self.dem = fractionNums[1]

        elif isinstance(fraction, int) or isinstance(fraction, float):
            fractionNums = self.numToFraction(fraction)
            self.num = fractionNums[0]
            self.dem = fractionNums[1]
            
        else:
            raise TypeError(f'cannot parse type {type(fraction)}')

        self.simplify()

    #Get the greatest common divisor of the numerator and denominator
    @property
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

        #print(f'GCD is {abs(num2)}') #debug
        return abs(num2)

    #Simplify the fraction
    def simplify(self):
        #print(f'simplifying {self}') #debug
        num = self.num
        dem = self.dem

        #Ensure that negatives are represented in the numerator and there is no double negative
        if dem < 0:
            #print('flipping negatives') #debug
            num = -num
            dem = -dem

        num /= self.GCD
        dem /= self.GCD

        self.num = int(num)
        self.dem = int(dem)

    #Simplify a given fraction in list form
    def simplifyNums(nums):
        return Fraction(nums, True).nums

    #Automatically simplify fractions
    def autoSimplify(func):
        def inner(*args, **kwargs):
            fraction = func(*args, **kwargs)
            fraction.simplify
            return fraction
        return inner

    #Output the numbers as a fraction
    def __str__(self):
        return (f'{self.num}/{self.dem}')

    #Output the fraction as an int
    def __int__(self):
        return int(self.num / self.dem)

    #Output the fraction as a float
    def __float__(self):
        return self.num / self.dem

    #Adds two given fractions
    def add(self, fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) + (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Subtracts two given fractions
    def sub(self, fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) - (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Multiplies two given fractions
    def mul(self, fraction1, fraction2):
        num = fraction1.num * fraction2.num
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Divides two given fractions
    def truediv(self, fraction1, fraction2):
        num = fraction1.num * fraction2.dem
        dem = fraction1.dem * fraction2.num

        return Fraction([num, dem])

    #Adds another fraction to this one and returns a new fraction
    def __add__(self, other):
        return self.add(self, other)

    #Subtracts another fraction from this one and returns a new fraction
    def __sub__(self, other):
        return self.sub(self, other)

    #Multiplies another fraction by this one and returns a new fraction
    def __mul__(self, other):
        return self.mul(self, other)

    #Divides this fraction by another one and returns a new fraction
    def __truediv__(self, other):
        return self.mul(self, other)

    #Adds another fraction to this one and returns a new fraction
    def __radd__(self, number):
        #print(f'adding self to {number}') #debug
        other = self.numToFraction(number)
            
        return self.add(other, self)

    #Subtracts another fraction from this one and returns a new fraction
    def __rsub__(self, number):
        #print(subtracting self from {number}') #debug
        other = self.numToFraction(number)
            
        return self.sub(other, self)

    #Multiplies another fraction by this one and returns a new fraction
    def __rmul__(self, number):
        #print(multiplying {number} by self') #debug
        other = self.numToFraction(number)
        
        return self.mul(other, self)

    #Divides this fraction by another one and returns a new fraction
    def __rtruediv__(self, number):
        #print(dividing {number} by self') #debug
        other = self.numToFraction(number)
        
        return self.truediv(other, self)

    #Adds this fraction to another one and replaces this fraction with the result
    def __iadd__(self, other):
        answer = self.add(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Subtracts another fraction from this one and replaces this fraction with the result
    def __isub__(self, other):
        answer = self.sub(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Multiplies this fraction by another one and replaces this fraction with the result
    def __imul__(self, other):
        answer = self.mul(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Divides this fraction by another one and replaces this fraction with the result
    def __itruediv__(self, other):
        answer = self.truediv(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Flips this fraction between positive and negative
    def __neg__(self):
        return Fraction([-self.num, self.dem])

    #Updates this fraction to its reciprocal
    def invert(self):
        return Fraction([self.dem, self.num])

    #Returns either the numerator or denominator, as if the fraction were a list in form [num, dem]
    def __getitem__(self, index):
        if index == 0:
            return self.num
        elif index == 1:
            return self.dem
        else:
            raise IndexError: f'Invalid value for index: {index}. Must be 0 or 1'
    
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

    #Sets the fraction to the top-heavy form of a given mixed fraction
    @mixed.setter
    def mixed(self, fraction):
        #Fraction given in form [integerPart, [num, dem]]
        fraction[1][0] += fraction[0] * fraction[1][1]
        self.num = fraction[1][0]
        self.dem = fraction[1][1]

    #Returns a list of the numerator and denominator
    @property
    def nums(self):
        return ([self.num, self.dem])

    #Updates the fraction through the use of nums
    @nums.setter
    def nums(self, numsList):
        self.num = numsList[0]
        self.dem = numsList[1]

        self.simplify()

    def numToFraction(self, number):
        if round(number, 0) == number:
            return [number, 0]
        else:
            decPlaces = len(str(number)[re.search(r'\.', str(number)).start() + 1:])
            number *= 10 ** decPlaces

            return Fraction([number, 10 ** decPlaces])
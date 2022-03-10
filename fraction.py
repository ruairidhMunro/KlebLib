class Fraction:
    def __init__(self, fraction, listInput=False):
        if listInput:
            if not isinstance(fraction, list):
                raise ValueError(f'Expected list, got {type(fraction)}')
            self.num = fraction[0]
            self.dem = fraction[1]
        else:
            if not isinstance(fraction, str):
                raise ValueError(f'Expected str, got {type(polynomial)}')
            fraction_nums = fraction.split('/')
            map_object = map(int, fraction_nums)
            fraction_nums = list(map_object)
            self.num = fraction_nums[0]
            self.dem = fraction_nums[1]

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

        #print(f'GCD is {num2}') #debug
        return num2

    #Simplify the fraction
    def simplify(self):
        num = self.num
        dem = self.dem

        #Ensure that negatives are represented in the numerator and there is no double negative
        if dem < 0:
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
    def output(self):
        return (f'{self.num}/{self.dem}')

    #Output the fraction as a float
    def outputFloat(self):
        return self.num / self.dem

    #Adds another fraction to this one and returns a new fraction
    def __add__(self, fraction2):
        num = (self.num * fraction2.dem) + (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Subtracts another fraction from this one and returns a new fraction
    def __sub__(self, fraction2):
        num = (self.num * fraction2.dem) - (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Multiplies another fraction by this one and returns a new fraction
    def __mul__(self, fraction2):
        num = self.num * fraction2.num
        dem = self.dem * fraction2.dem

        return Fraction([num, dem], True)

    #Divides this fraction by another one and returns a new fraction
    def __truediv__(self, fraction2):
        num = self.num * fraction2.dem
        dem = self.dem * fraction2.num

        return Fraction([num, dem], True)

    #Adds this fraction to another one and replaces this fraction with the result
    def __iadd__(self, fraction2):
        num = (self.num * fraction2.dem) + (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        simplified = simplifyNums([num, dem])
        
        self.num = simplified[0]
        self.dem = simplified[1]
        return self

    #Subtracts another fraction from this one and replaces this fraction with the result
    def __isub__(self, fraction2):
        num = (self.num * fraction2.dem) - (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        simplified = simplifyNums([num, dem])
        
        self.num = simplified[0]
        self.dem = simplified[1]
        return self

    #Multiplies this fraction by another one and replaces this fraction with the result
    def __imul__(self, fraction2):
        num = self.num * fraction2.num
        dem = self.dem * fraction2.dem

        simplified = simplifyNums([num, dem])
        
        self.num = simplified[0]
        self.dem = simplified[1]
        return self

    #Divides this fraction by another one and replaces this fraction with the result
    def __itruediv__(self, fraction2):
        num = self.num * fraction2.dem
        dem = self.dem * fraction2.num

        simplified = simplifyNums([num, dem])
        
        self.num = simplified[0]
        self.dem = simplified[1]
        return self

    #Flips this fraction between positive and negative
    def __neg__(self):
        self.num = -self.num
        return self
    
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
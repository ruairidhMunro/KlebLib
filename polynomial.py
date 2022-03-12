import re

class Polynomial:
    def __init__(self, polynomial, dictInput=False):
        if dictInput:
            if not isinstance(polynomial, dict):
                raise ValueError(f'Expected dict, got {type(polynomial)}')
            self.polynomial = polynomial
        else:
            if not isinstance(polynomial, str):
                raise ValueError(f'Expected str, got {type(polynomial)}')
            self.polynomial = self.parse(polynomial)

    def parse(self, polynomial):
        #print(f'parsing polynomial {polynomial}') #debug
        negatives = []
        additions = re.finditer(r'[\+-]', polynomial)
        startNegative = re.search(r'^[\+-]', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negatives.append(i)
                else:
                    negatives.append(i + 1)

        terms = re.split(r'[\+-]', polynomial)
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
                    if term: #If there is a coefficient
                        polynomial[1] = float(term) * negativeMultiple
                    else:
                        polynomial[1] = 1
            else:
                polynomial[0] = float(term) * negativeMultiple

        return polynomial

    def differentiate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            if coefficient * exponent != 0:  #If the coefficient will not be 0
                polynomial[exponent - 1] = coefficient * exponent

        return Polynomial(polynomial, True)

    def integrate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            polynomial[exponent + 1] = coefficient / (exponent + 1)

        return Polynomial(polynomial, True)

    def integrateDefinite(self, min, max):
        expr = self.integrate()
        upper = lower = 0

        for exponent, coefficient in expr.items():
            upper += coefficient * max ** exponent
            lower += coefficient * min ** exponent

        result = max - min
        return result

    def __add__(self, other):
        returnPolynomial = self.polynomial.copy()
        for exponent, coefficient in other.polynomial.items():
            if exponent in returnPolynomial.keys():
                returnPolynomial[exponent] += coefficient
            else:
                returnPolynomial[exponent] = coefficient

        return Polynomial(returnPolynomial, True)

    def __sub__(self, other):
        returnPolynomial = self.polynomial.copy()
        for exponent, coefficient in other.polynomial.items():
            if exponent in returnPolynomial.keys():
                returnPolynomial[exponent] -= coefficient
            else:
                returnPolynomial[exponent] = -coefficient

        return Polynomial(returnPolynomial, True)

    def __iadd__(self, other):
        for exponent, coefficient in other.polynomial.items():
            if exponent in self.polynomial.keys():
                self.polynomial[exponent] += coefficient
            else:
                self.polynomial[exponent] = coefficient

        return self

    def __isub__(self, other):
        for exponent, coefficient in other.polynomial.items():
            if exponent in self.polynomial.keys():
                self.polynomial[exponent] -= coefficient
            else:
                self.polynomial[exponent] = -coefficient

        return self

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
            output = ''
            i = 0
            for exponent, coefficient in self.polynomial.items():
                if coefficient < 0:
                    if i == 0:
                        output += '-'
                    else:
                        output += ' - '
                elif i != 0:
                    output += ' + '

                if exponent > 1 or exponent < 0:
                    output += f'{abs(coefficient)}x^{exponent}'
                elif exponent == 1:
                    output += f'{abs(coefficient)}x'
                else:
                    output += f'{abs(coefficient)}'

                i += 1

            return output
        else:
            return self.polynomial

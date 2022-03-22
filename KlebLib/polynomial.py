import re

class Polynomial:
    def __init__(self, polynomial):
        #print(f'the polynomials are {polynomials} and are of type {type(polynomials)}') #debug
        if type(polynomial) is list:
            self.polynomial = polynomial
        else:
            self.polynomial = self.parse(polynomial, self.getVariables(polynomial))
        #print(self.polynomials) #debug

    def parse(self, polynomial, variables):
        #print(f'multivar parsing {polynomial} with variables {variables}') #debug

        output = []
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

        #print(f'the terms are {terms}') #debug
        #print(f'the negatives are {negatives}') #debug

        for i, term in enumerate(terms):
            term = term.strip()
            #print(f'parsing term {term} at position {i}') #debug
            
            currentTerm = {}
                
            if i in negatives:
                negativeMultiple = -1
            else:
                negativeMultiple = 1
                        
            for variable in self.getVariables(term):
                if f'{variable}^' in term:
                    currentTerm[variable] = self.trimNum(term, 'right')
                            
                else: #If it has no exponent
                    currentTerm[variable] = 1

            trimmed = self.trimNum(term, 'left')
            if trimmed: #If there is a coefficient
                currentTerm['num'] = trimmed * negativeMultiple
            else:
                currentTerm['num'] = negativeMultiple

            if currentTerm:
                output.append(currentTerm)

        return output

    def differentiate(self, partial=False, varToDiff=''):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            if coefficient * exponent != 0:  #If the coefficient will not be 0
                polynomial[exponent - 1] = coefficient * exponent

        return Polynomial(polynomial, True)

    def integrate(self, varToIntegrate=''):
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
        print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = self.polynomial.copy()
        for i, term in enumerate(other.polynomial.copy()):
            print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if location:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        return Polynomial(outputPolynomial)

    def __sub__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __str__(self):
        '''
        output = ''

        i = 0
        for variable, terms in self.polynomial.items():
            if variable == 'num':
                if terms < 0:
                    if i == 0:
                        output += str(self.intIfPos(terms))
                    else:
                        output += f' - {self.intIfPos(abs(terms))}'
                else:
                    output += str(self.intIfPos(terms))

                i += 1
            elif variable == 'links':
                pass
            else:
                for exponent, coefficient in terms.items():
                    if coefficient < 0:
                        if i == 0:
                            output += '-'
                        else:
                            output += ' - '
                    elif i != 0:
                        output += ' + '
        
                    if exponent > 1 or exponent < 0:
                        if coefficient != 1:
                            output += f'{self.intIfPos(abs(coefficient))}{variable}^{self.intIfPos(exponent)}'
                        else:
                            output += f'{variable}^{self.intIfPos(exponent)}'
                    elif exponent == 1:
                        if coefficient != 1:
                            output += f'{self.intIfPos(abs(coefficient))}{variable}'
                        else:
                            output += variable
        
                    i += 1
        '''

        output = str(self.polynomial)

        return output

    def intIfPos(self, num):
        if int(num) == num:
            return int(num)
        else:
            return(num)

    def getVariables(self, polynomial):
        variables = set()
        try:
            for character in polynomial:
                #If it is a letter
                if (ord(character) >= 65 and ord(character) <= 90) or (ord(character) >= 97 and ord(character) <= 122):
                    variables.add(character)
        #If polynomial is not a string
        except TypeError:
            return []

        return list(variables)

    def trimNum(self, string, side):
        #print(f'trimming {string}') #debug
        if side == 'left':
            lastChar = 0
            for i, char in enumerate(string):
                try:
                    float(char)
                except ValueError:
                    break
                else:
                    lastChar = i

            try:
                #print(f'joining {string[0:lastChar+1]} after {side} trim') #debug
                return float(''.join(string[0:lastChar+1]))
            except ValueError:
                return None

        else:
            tempString = string[::1]
            lastChar = len(string) - 1

            i = lastChar
            for char in tempString:
                try:
                    float(char)
                except ValueError:
                    break
                else:
                    lastChar = i
                i -= 1

            try:
                #print(f'joining {string[lastChar:]} after {side} trim') #debug
                return float(''.join(string[lastChar:]))
            except ValueError:
                return None

    def locate(self, polynomial, searchTerm):
        print(f'locating term {searchTerm} in polynomial {polynomial}') #debug
        del searchTerm['num']
        for i, term in enumerate(polynomial):
            del term['num']
            if searchTerm == term:
                print(f'found term') #debug
                return i
        print('didn\'t find term') #debug
        return False
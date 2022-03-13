import re

class Polynomial:
    def __init__(self, polynomial):
        #print(f'the polynomials are {polynomials} and are of type {type(polynomials)}') #debug
        #print(f'dictInput is {dictInput}') #debug
        if type(polynomial) is dict:
            self.polynomial = polynomial
        else:
            self.polynomial = self.parse(polynomial, self.getVariables(polynomial))
        #print(self.polynomials) #debug

    def parse(self, polynomial, variables):
        #print(f'multivar parsing {polynomial} with variables {variables}') #debug

        output = {}
        negativesList = []
        negatives = {}
        additions = re.finditer(r'[\+-]', polynomial)
        startNegative = re.search(r'^[\+-]', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negativesList.append(i)
                else:
                    negativesList.append(i + 1)

        termsList = re.split(r'[\+-]', polynomial)
        if startNegative:
            #print('removed first term') # debug
            del terms[0]
        terms = {}
        for variable in variables:
            terms[variable] = []
            negatives[variable] = []
            lenCurrentTerms = 0
            
            for i, term in enumerate(termsList):
                if variable in term:
                    terms[variable].append(term.strip())
                    if i in negativesList:
                        negatives[variable].append(lenCurrentTerms)
                    lenCurrentTerms += 1

        terms['num'] = 0
        lenCurrentTerms = 0
        
        for i, term in enumerate(termsList):
            try:
                float(term)
            except ValueError:
                pass
            else:        
                if i in negativesList:
                    terms['num'] -= float(term)
                else:
                    terms['num'] += float(term)
                lenCurrentTerms += 1

        #print(f'the terms are {terms}') #debug
        #print(f'the negatives are {negatives}') #debug

        for variable, varTerms in terms.items():
            #print(f'parsing variable {variable} with terms {varTerms}')
            if variable == 'num':
                output[variable] = terms['num']
            else:
                output[variable] = {}
                
                for i, term in enumerate(varTerms):
                    if i in negatives[variable]:
                        negativeMultiple = -1
                    else:
                        negativeMultiple = 1
                        
                    if variable in term:
                        if '^' in term:
                            term = term.split(f'{variable}^')
                            try:
                                output[variable][float(term[1])] = float(term[0]) * negativeMultiple
                            except ValueError: #If there is no coefficient
                                output[variable][float(term[1])] = negativeMultiple
                        else: #If it has no exponent
                            term = term[:-1]
                            if term: #If there is a coefficient
                                output[variable][1] = float(term) * negativeMultiple
                            else:
                                output[variable][1] = 1
                    else: #If it is just a number
                        output[variable].append(float(term) * negativeMultiple)

        return output

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
        outputPolynomial = self.polynomial.copy()
        for variable, terms in other.polynomial.items():
            #print('adding polynomials') #debug
            #print(f'the variable is {variable}') #debug
            #print(f'the terms are {terms}') #debug
            
            if variable in self.polynomial.keys():
                if variable == 'num':
                    outputPolynomial['num'] += other.polynomial['num']
                else:
                    for exponent, coefficient in terms.items():
                        if exponent in self.polynomial[variable]:
                            outputPolynomial[variable][exponent] += coefficient
                        else:
                            outputPolynomial[variable][exponent] = coefficient
            else:
                outputPolynomial[variable] = terms

        return Polynomial(outputPolynomial)

    def __sub__(self, other):
        outputPolynomial = self.polynomial.copy()
        for variable, terms in other.polynomial.items():
            #print('subtracting polynomials') #debug
            #print(f'the variable is {variable}') #debug
            #print(f'the terms are {terms}') #debug
            
            if variable in self.polynomial.keys():
                if variable == 'num':
                    outputPolynomial['num'] -= other.polynomial['num']
                else:
                    for exponent, coefficient in terms.items():
                        if exponent in self.polynomial[variable]:
                            outputPolynomial[variable][exponent] -= coefficient
                        else:
                            outputPolynomial[variable][exponent] = -coefficient
            else:
                outputPolynomial[variable] = {}
                for exponent, coefficient in terms.items():
                    outputPolynomial[variable][exponent] = -coefficient

        return Polynomial(outputPolynomial)

    def __iadd__(self, other):
        outputPolynomial = self.polynomial.copy()
        for variable, terms in other.polynomial.items():
            #print('adding polynomials') #debug
            #print(f'the variable is {variable}') #debug
            #print(f'the terms are {terms}') #debug
            
            if variable in self.polynomial.keys():
                if variable == 'num':
                    outputPolynomial['num'] += other.polynomial['num']
                else:
                    for exponent, coefficient in terms.items():
                        if exponent in self.polynomial[variable]:
                            outputPolynomial[variable][exponent] += coefficient
                        else:
                            outputPolynomial[variable][exponent] = coefficient
            else:
                outputPolynomial[variable] = terms

        self.polynomial = outputPolynomial
        return self

    def __isub__(self, other):
        outputPolynomial = self.polynomial.copy()
        for variable, terms in other.polynomial.items():
            #print('subtracting polynomials') #debug
            #print(f'the variable is {variable}') #debug
            #print(f'the terms are {terms}') #debug
            
            if variable in self.polynomial.keys():
                if variable == 'num':
                    outputPolynomial['num'] -= other.polynomial['num']
                else:
                    for exponent, coefficient in terms.items():
                        if exponent in self.polynomial[variable]:
                            outputPolynomial[variable][exponent] -= coefficient
                        else:
                            outputPolynomial[variable][exponent] = -coefficient
            else:
                outputPolynomial[variable] = {}
                for exponent, coefficient in terms.items():
                    outputPolynomial[variable][exponent] = -coefficient

        self.polynomial = outputPolynomial
        return self

    def __str__(self):
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

        return output

    def intIfPos(self, num):
        if int(num) == num:
            return int(num)
        else:
            return(num)
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
        #print(f'parsing polynomial {polynomial
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
                
            #Check if term should be negative
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

    def differentiate(self, varToDiff):
        outputPolynomial = []
        for term in self.polynomial:
            termToEdit = {}
            edited = False
            for variable, exponent in term.items():
                if variable == varToDiff:
                    termToEdit['num'] = term['num'] * exponent
                    if exponent - 1 != 0:
                        termToEdit[variable] = exponent - 1
                    edited = True
                elif variable != 'num':
                    termToEdit[variable] = exponent
            if not edited:
                termToEdit['num'] = term['num']

            outputPolynomial.append(termToEdit)

        return Polynomial(outputPolynomial)

    def integrate(self, varToIntegrate):
        outputPolynomial = []
        for term in self.polynomial:
            termToEdit = {}
            edited = False
            for variable, exponent in term.items():
                if variable == varToIntegrate:
                    termToEdit['num'] = term['num'] / (exponent + 1)
                    termToEdit[variable] = exponent + 1
                    edited = True
                elif variable != 'num':
                    termToEdit[variable] = exponent
            if not edited:
                termToEdit['num'] = term['num']
                termToEdit[varToIntegrate] = 1

            outputPolynomial.append(termToEdit)

        return Polynomial(outputPolynomial)

    def integrateDefinite(self, varToIntegrate, max, min):
        integrated = self.integrate(varToIntegrate)
        outputs = [[], []]
        limits = [max, min]

        for i, output in enumerate(outputs):
            for term in integrated.polynomial:
                outputTerm = {}
                edited = False
                for variable, exponent in term.items():
                    if variable == varToIntegrate:
                        outputTerm['num'] = term['num'] * limits[i] ** exponent
                        edited = True
                    elif variable != 'num':
                        outputTerm[variable] = exponent

                if not edited:
                    outputTerm['num'] = term['num']

                output.append(outputTerm)

            #print(f'output {i} before cleanup is {output}') #debug
            output = self.consolidate(output)
            #print(f'output {i} after cleanup is {output}') #debug

        upper = Polynomial(outputs[0])
        lower = Polynomial(outputs[1])

        return upper - lower

    def __add__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = self.polynomial.copy()
        for i, term in enumerate(other.polynomial):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if location:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        return Polynomial(self.consolidate(outputPolynomial))

    def __sub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = self.polynomial.copy()
        for i, term in enumerate(other.polynomial):
            #print(f'subtracting term {term} from polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if location:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        return Polynomial(self.consolidate(outputPolynomial))

    def __iadd__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = self.polynomial.copy()
        for i, term in enumerate(other.polynomial):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if location:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        self.polynomial = self.consolidate(outputPolynomial)
        return self

    def __isub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = self.polynomial.copy()
        for i, term in enumerate(other.polynomial):
            #print(f'suntracting term {term} from polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if location:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        self.polynomial = self.consolidate(outputPolynomial)
        return self

    def __str__(self):
        output = ''

        i = 0
        for term in self.polynomial:
            if term['num'] < 0:
                if i == 0:
                    output += f'-{self.intIfPos(abs(term["num"]))}'
                else:
                    output += f' - {self.intIfPos(abs(term["num"]))}'
            elif i != 0:
                output += f' + {self.intIfPos(term["num"])}'

            i += 1
                
            for variable, exponent in term.items():
                if variable != 'num':
                    if exponent == 1:
                        output += str(variable)
                    else:
                        output += f'({variable}^{self.intIfPos(exponent)})'
                
        return output

    def intIfPos(self, num):
        try:
            assert int(num) == num
        except AssertionError:
            return num
        except ValueError:
            return num
        else:
            return int(num)

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
        #print(f'locating term {searchTerm} in polynomial {polynomial}') #debug
        del searchTerm['num']
        for i, term in enumerate(polynomial):
            termToEdit = term.copy()
            del termToEdit['num']
            if searchTerm == termToEdit:
                #print('found term') #debug
                return i
        #print('didn\'t find term') #debug
        return False

    def consolidate(self, polynomial):
        output = polynomial.copy()
        termsToRemove = []
        
        total = 0
        for term in output:
            numVars = 0
            for variable in term:
                if variable != 'num':
                    numVars += 1

            if numVars == 0:
                total += term['num']
                termsToRemove.append(term)

        if total:
            output.append({'num': total})

        for term in termsToRemove:
            del output[output.index(term)]

        return output
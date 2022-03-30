import re

class Polynomial:
    def __init__(self, polynomial):
        #print(f'the polynomials are {polynomials} and are of type {type(polynomials)}') #debug
        if type(polynomial) is list:
            for term in polynomial:
                if not 'num' in term:
                    raise KeyError('Every term must contain key \'num\'')
            self.polynomial = polynomial
        else:
            self.polynomial = self.parse(polynomial, self.getVariables(polynomial))
        #print(self.polynomials) #debug

    def parse(self, polynomial, variables):
        #parse the polynomial into a list of dictionaries
        
        output = []
        #print(f'parsing polynomial {polynomial}') #debug
        negatives = []
        additions = re.finditer(r'(\s\+\s)|(\s-\s)', polynomial)
        startNegative = re.search(r'^-', polynomial)
        if startNegative:
            negatives.append(0)
            polynomial = polynomial[1:]

        for i, match in enumerate(additions):
            #print(f'the match at position {i} is {match.group()}') #debug
            if match.group() == ' - ':
                negatives.append(i + 1)

        terms = re.split(r'\s+[+-]\s+', polynomial)
        #print(f'the terms before translation are {terms}') #debug
        terms = [self.translateSuper(i) for i in terms]
        #print(f'the terms after translation are {terms}') #debug
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
                continue

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
        outputPolynomial = self.copy(self.polynomial)
        
        for i, term in enumerate(other.polynomial.copy()):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        return Polynomial(self.consolidate(outputPolynomial))

    def __sub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = self.copy(self.polynomial)
        
        for i, term in enumerate(other.polynomial.copy()):
            #print(f'subtracting term {term} from polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        return Polynomial(self.consolidate(outputPolynomial))

    def __iadd__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = self.copy(self.polynomial)
        
        for i, term in enumerate(other.polynomial.copy()):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        self.polynomial = self.consolidate(outputPolynomial)
        return self

    def __isub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = self.copy(self.polynomial)
        
        for i, term in enumerate(other.polynomial.copy()):
            #print(f'suntracting term {term} from polynomial {outputPolynomial}') #debug
            location = self.locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        self.polynomial = self.consolidate(outputPolynomial)
        return self

    def __str__(self):
        output = ''

        i = 0
        for term in self.polynomial:
            if term['num'] < 0:
                if term['num'] != -1:
                    if i == 0:
                        output += f'-{self.intIfPos(abs(term["num"]))}'
                    else:
                        output += f' - {self.intIfPos(abs(term["num"]))}'
                else:
                    if i == 0:
                        output += '-'
                    else:
                        output += ' + '
            elif i != 0:
                if term['num'] == 1:
                    output += ' + '
                else:
                    output += f' + {self.intIfPos(term["num"])}'
            elif term['num'] != 1:
                output += str(self.intIfPos(term['num']))

            i += 1
                
            for variable, exponent in term.items():
                if variable != 'num':
                    if exponent == 1:
                        output += str(variable)
                    else:
                        output += variable + self.super(self.intIfPos(exponent))
                
        return output

    def __getitem__(self, variable):
        output = []
        
        for term in self.polynomial:
            if variable in term:
                output.append(term.copy())

        return Polynomial(output)

    def __eq__(self, other):
        equal = True

        for term in self.polynomial:
            #print(f'comparing term {term} from self') #debug
            if term not in other.polynomial:
                #print(f'didn\'t find term {term} in other') #debug
                equal = False
                
        for term in other.polynomial:
            #print(f'comparing term {term} from other') #debug
            if term not in self.polynomial:
                #print(f'didn\'t find term {term} in self') #debug
                equal = False

        return equal

    def intIfPos(self, num):
        #print(f'checking if {num} can be int') #debug
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
        numPos = self.getNumPos(string, side)

        if numPos:
            #print(f'num found between positions {numPos.start()} and {numPos.end()}') #debug
            return float(string[numPos[0]:numPos[1]])
        else:
            #print(f'num not found') #debug
            return 0

    def getNumPos(self, string, side):
        if side == 'left':
            numPos = re.search(r'^-?\d+\.?\d*', string)
        else:
            numPos = re.search(r'-?\d+\.?\d*$', string)

        if numPos:
            return [numPos.start(), numPos.end()]
        else:
            return None

    def locate(self, polynomial, searchTerm):
        #print(f'locating term {searchTerm} in polynomial {polynomial}') #debug
        del searchTerm['num']
        for i, term in enumerate(polynomial):
            termToEdit = term.copy()
            del termToEdit['num']
            if searchTerm == termToEdit:
                #print(f'found term at position {i}') #debug
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

    def copy(self, listToCopy):
        output = []
        
        for item in listToCopy:
            output.append(item.copy())

        return output

    def super(self, num):
        superscriptMap = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}

        return self.translate(str(num), superscriptMap)

    def translateSuper(self, string):
        #print(f'translating {string}') #debug
        superscriptMap = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}

        superscriptMap = {v:k for (k, v) in superscriptMap.items()}

        string = self.translate(string, superscriptMap)

        num = self.trimNum(string, 'right')
        numPos = self.getNumPos(string, 'right')

        if numPos:
            if numPos[0] == 0:
                return string
            if string[numPos[0] - 1] == '^':
                return string[:numPos[0]] + str(num)
            else:
                return string[:numPos[0]] + '^' + str(num)
        else:
            return string
        
    def translate(self, string, table):
        trans = str.maketrans(
            ''.join(table.keys()),
            ''.join(table.values())
        )

        return string.translate(trans)
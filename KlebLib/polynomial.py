import re
from typing import Union
from copy import deepcopy

__all__ = ['Polynomial']

def get_variables(polynomial:Union[list, str]) -> list:
    variables = set()

    if type(polynomial) is str:
        for character in polynomial:
            #If it is a letter
            if (ord(character) >= 65 and ord(character) <= 90) or (ord(character) >= 97 and ord(character) <= 122):
                variables.add(character)

    elif type(polynomial) is list:
        for term in polynomial:
            for variable in term:
                if variable != 'num':
                    variables.add(variable)

    return list(variables)

class Polynomial:
    def __init__(self, polynomial:Union[list, str]):
        #print(f'the polynomials are {polynomial} and are of type {type(polynomial).__name__}') #debug
        if type(polynomial) is list:
            for term in polynomial:
                if not 'num' in term:
                    raise KeyError('Every term must contain key \'num\'')
            self.polynomial = polynomial
        else:
            self.polynomial = self._parse(polynomial, get_variables(polynomial))
        #print(self.polynomial) #debug

    def _parse(self, polynomial:str, variables:list) -> list:
        #parse the polynomial into a list of dictionaries
        
        #print(f'parsing polynomial {polynomial}') #debug
        output = []
        negatives = []
        additions = re.finditer(r'\s+[+-]\s+', polynomial)
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
        terms = [self._translate_super(i) for i in terms]
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
                        
            for variable in get_variables(term):
                if f'{variable}^' in term:
                    currentTerm[variable] = self._trim_num(term, 'right')
                            
                else: #If it has no exponent
                    currentTerm[variable] = 1

            trimmed = self._trim_num(term, 'left')
            if trimmed: #If there is a coefficient
                currentTerm['num'] = trimmed * negativeMultiple
            else:
                currentTerm['num'] = negativeMultiple

            if currentTerm:
                output.append(currentTerm)

        return output

    def differentiate(self, varToDiff:str=None):
        if varToDiff is None:
            #print(f'attempting to imply variable from polnomial with variables {self.get_variables(self.polynomial)}') #debug
            if len(self.get_variables(self.polynomial)) != 1:
                raise TypeError('cannot implicitly detect variable for polynomials of multiple variables')
            else:
                varToDiff = self.get_variables(self.polynomial)[0]
        
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

    def integrate(self, varToIntegrate:str=None):
        if varToIntegrate is None:
            if len(get_variables(self.polynomial)) != 1:
                raise TypeError('cannot implicitly detect variable for polynomials of multiple variables')
            else:
                varToIntegrate = get_variables(self.polynomial)[0]
                
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

    def integrate_definite(self, varToIntegrate:str, max:int, min:int):
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
            output = self._consolidate(output)
            #print(f'output {i} after cleanup is {output}') #debug

        upper = Polynomial(outputs[0])
        lower = Polynomial(outputs[1])

        return upper - lower

    def __add__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self._locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        return Polynomial(self._consolidate(outputPolynomial))

    def __sub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'subtracting term {term} from polynomial {outputPolynomial}') #debug
            location = self._locate(outputPolynomial.copy(), term.copy())
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
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = self._locate(outputPolynomial.copy(), term.copy())
            if not type(location) is bool:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        self.polynomial = self.consolidate(outputPolynomial)
        return self

    def __isub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'suntracting term {term} from polynomial {outputPolynomial}') #debug
            location = self._locate(outputPolynomial.copy(), term.copy())
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
                        output += f'-{self._int_if_pos(abs(term["num"]))}'
                    else:
                        output += f' - {self._int_if_pos(abs(term["num"]))}'
                else:
                    if i == 0:
                        output += '-'
                    else:
                        output += ' + '
            elif i != 0:
                if term['num'] == 1:
                    output += ' + '
                else:
                    output += f' + {self._int_if_pos(term["num"])}'
            elif term['num'] != 1:
                output += str(self._int_if_pos(term['num']))

            i += 1
                
            for variable, exponent in term.items():
                if variable != 'num':
                    if exponent == 1:
                        output += str(variable)
                    else:
                        output += variable + self._super(self._int_if_pos(exponent))
                
        return output

    def __repr__(self):
        return f'polynomial.Polynomial({self.polynomial})'

    def __float__(self):
        temp = self.polynomial[0].copy()
        del temp['num']
        
        if len(self.polynomial) == 1 and not temp:
            return float(self.polynomial[0]['num'])
        else:
            raise ValueError('cannot convert polynomial with variables to float')

    def __int__(self):
        try:
            return int(float(self))
        except ValueError:
            raise ValueError('cannot convert polynomial with variables to int')

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

    def _int_if_pos(self, num:Union[float, str]) -> Union[int, float, str]:
        #print(f'checking if {num} can be int') #debug
        try:
            assert int(num) == num
        except AssertionError:
            return num
        except ValueError:
            return num
        else:
            return int(num)

    def _trim_num(self, string:str, side:str) -> float:
        #print(f'trimming {string}') #debug
        numPos = self._get_num_pos(string, side)

        if numPos:
            #print(f'num found between positions {numPos.start()} and {numPos.end()}') #debug
            return float(string[numPos[0]:numPos[1]])
        else:
            #print(f'num not found') #debug
            return 0.0

    def _get_num_pos(self, string:str, side:str) -> Union[list, None]:
        if side == 'left':
            numPos = re.search(r'^-?\d+\.?\d*', string)
        else:
            numPos = re.search(r'-?\d+\.?\d*$', string)

        if numPos:
            return [numPos.start(), numPos.end()]
        else:
            return None

    def _locate(self, polynomial:list, searchTerm:dict) -> Union[int, bool]:
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

    def _consolidate(self, polynomial:list) -> list:
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

    def _super(self, num:str) -> str:
        superscriptMap = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}

        return self._translate(str(num), superscriptMap)

    def _translate_super(self, string:str) -> str:
        #print(f'translating {string}') #debug
        superscriptMap = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}

        superscriptMap = {v:k for (k, v) in superscriptMap.items()}

        string = self._translate(string, superscriptMap)

        num = self._trim_num(string, 'right')
        numPos = self._get_num_pos(string, 'right')

        if numPos:
            if numPos[0] == 0:
                return string
            if string[numPos[0] - 1] == '^':
                return string[:numPos[0]] + str(num)
            else:
                return string[:numPos[0]] + '^' + str(num)
        else:
            return string
        
    def _translate(self, string:str, table:dict) -> str:
        trans = str.maketrans(
            ''.join(table.keys()),
            ''.join(table.values())
        )

        return string.translate(trans)
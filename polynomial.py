import re

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
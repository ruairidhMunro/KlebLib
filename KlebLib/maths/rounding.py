"""ceiling -- round a number up to a specified number of decimal places
round -- round a number to the closest value at the specified number of decimal places
"""
def ceiling(num:float, decPlaces:int=0) -> float:
    """Rounds up.
    
    Arguments:
    num -- the number to be rounded
    decPlaces -- the number of decimal places to round to (default 0)
    """
    #Check validity of input
    if not isinstance(num, int) and not isinstance(num, float):
        raise ValueError(f'Expected int or float, got {type(num).__name__}')
    if not isinstance(decPlaces, int):
        raise ValueError(f'Expected int, got {type(decPlaces).__name__}')
    
    #Set up variables
    overflow = False
    num = str(num)
    numDigits = [i for i in num]
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
        
    return float(num)
    
def round(num:float, decPlaces:int=0) -> float:
    """Rounds to the closest number.
    
    Arguments:
    num -- the number to be rounded
    decPlaces -- the number of decimal places to round to (default 0)
    """
    if int(str(num)[decPlaces + 1]) >= 5:
        return ceiling(num, decPlaces)
    else:
        return round(num, decPlaces)
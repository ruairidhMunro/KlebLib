def ceiling(num, decPlaces=0):
    #Set up variables
    overflow = False
    num = str(num)
    numDigits = []
    for digit in num:
        numDigits.append(digit)
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
    num = float(num)
    return num
    
def smartRound(num, decPlaces):
    if str(num)[decPlaces + 1] >= 5:
        return ceiling(num)
    else:
        return round(num, 0)
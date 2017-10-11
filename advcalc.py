import sys
from calculator import Calculator


def getRawInput():
    print()
    print('Enter a mathematical expression in natural format.')
    print('Example: ((1 + 1) * 2) / 3 ')
    rawInput = None
    while(rawInput is None or len(rawInput) == 0):
        if (rawInput is not None and len(rawInput) == 0):
            print('Type "exit" to end.')
            print()
        rawInput = input('--> ')
    if rawInput == 'exit':
        exit()
    print('Your input was: ', str(rawInput))
    return rawInput


# Main
if (sys.version_info <= (3, 0)):
    print("Please use python version 3.0 or above.")
    exit()

print('========================')
print('    Calulator 0.0.1A    ')
print('   Type "exit" to end   ')
print('========================')

precision = None
while(precision is None or not isinstance(precision, int)
      or precision < 0 or precision > 28):
    print('Level of Precision? (1-28)')
    isPrecision = input('--> ')
    if len(isPrecision) == 0:
        continue

    precision = int(isPrecision)

debug = None
while(debug is None or not isinstance(debug, bool)):
    print('Debug Info? y(1) n(0)')
    isDebug = input('--> ').lower()
    if len(isDebug) == 0:
        continue

    debug = isDebug == 'yes' if len(isDebug) > 1 else bool(isDebug)

while(True):
    rawInput = getRawInput()
    rawInput = rawInput.replace(' ', '')
    rawInput += '='

    errors = Calculator.validateInput(rawInput)
    hadErrors = False
    for key in errors:
        error = errors[key]
        if len(error) > 0:
            print(error)
            hadErrors = True
        else:
            continue
    if hadErrors:
        continue

    try:
        calc = Calculator(rawInput, debug=True, precision=precision)
        print('Parsed Input was: {0}'.format(''.join(str(i) for i in
                                             calc.parsedInput)))
    except TypeError:
        print('ERR: TypeError in input!')
        continue
    except NameError:
        print('ERR: NameError in input!')
        continue

    print('ANS: ' + str(calc()))
    continue

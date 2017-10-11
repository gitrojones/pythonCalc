import re
import decimal


class Calculator:
    """Calculator class responsible for implementing\
    syntax checks, calculation functions and format rules."""

    # Must define a method to handle new operator (in ascending order)
    supportedOperators = '^/*+-' + '='
    orderOfOperations = {
        '^': 0,
        '/': 1,
        '*': 1,
        '+': 2,
        '-': 3
    }
    # Regex Patterns
    paranPattern = '[\(]', '[\)]'
    numberPattern = '[0-9.]'

    debug = False

    # Assign rawInput for calculation
    def __init__(self, rawInput='', **kwargs):
        self.debug = kwargs['debug'] if 'debug' in kwargs else False
        if 'precision' in kwargs:
            decimal.getcontext().prec = kwargs['precision']
        # Escaped Operators
        self.ops = ''.join([r'\{0}|'.format(op)
                            for op in Calculator.supportedOperators])
        self.ops = self.ops[0:len(self.ops) - 1]
        # Order of Operations (asc)
        # self.orderOfOperations = {self.supportedOperators[i]: i for i in
        #                           range(0, len(self.supportedOperators))}
        # Matches
        self.numberMatch = '(' + self.numberPattern + '{1,})'
        self.paranMatch = '({0}'.format(self.paranPattern[0]) + '{0,})',\
                          '({0}'.format(self.paranPattern[1]) + '{0,})'
        self.operatorMatch = '({0})'.format(self.ops)
        self.characterMatch = r'[{0}{1}]'.format(''.join([r'\{0}'.format(op)
                                                 for op in Calculator.
                                                 supportedOperators]),
                                                 r'\(\)') + r'{1,}'
        self.inputMatch = '{0}(-?){1}{2}({3}){4}'\
            .format(self.paranMatch[0], self.numberMatch, self.paranMatch[1],
                    self.numberPattern + '{0,}', r'({0}|)()'.format(self.ops))
        # Operations
        self.rawInput = rawInput
        if (len(rawInput) > 0):
            self.parsedInput = self.parseInput()

    def __call__(self, rawInput=''):
        if len(rawInput) != 0:
            self.rawInput = rawInput

        self.parsedInput = self.parseInput()
        self.operations = self.formatInput()
        self.results = self.parseOperations()

        if self.debug:
            print('')
            print('---------')
            print('STATEMENT')
            print('---------')
            print('RawInput:')
            print(self.rawInput)
            print('ParsedInput:')
            print(self.parsedInput)
            print('Operations:')
            print(self.operations)
            print('')

        return self.results

    @staticmethod
    def power(x, y):
        return x ** y

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def divide(x, y):
        if y == 0:
            print('ERROR: Cannot divide by zero.')
            return None
        return x / y

    @staticmethod
    def nestOperationList(oList, nVal, rBefore, rAfter, before=False):
        nList = oList[rBefore]
        orderOps = oList[rAfter]
        if (before):
            orderOps.insert(0, decimal.Decimal(nVal))
            nList.extend(orderOps)
        else:
            orderOps.append(decimal.Decimal(nVal))
            nList.append(orderOps)
        return nList

    @staticmethod
    def handleMultiParan(parsedInput, index, paran):
        parens = re.findall('[\{0}]'.format(paran), parsedInput[index])
        print(parens)
        if (len(parens) > 1):
            parsedInput[index] = paran * (len(parens) - 1)
            return 0
        else:
            parsedInput.pop(index)
            return 1

    @staticmethod
    def traverse(o, tree_types=(list, tuple)):
        if isinstance(o, tree_types):
            for value in o:
                for subValue in Calculator.traverse(value, tree_types):
                    yield subValue
        else:
            yield o

    @staticmethod
    def raisePresedence(statements, offset=2):
        length = len(list(Calculator.traverse(statements)))
        diff = length - offset if length - offset > 0 else 0
        oList = statements
        count = 0

        # Fix for heavily nested operations
        if(offset == 1):
            return

        while(True):
            if (isinstance(oList[len(oList) - 1], list)):
                oList = oList[len(oList) - 1]
            if (count <= diff):
                break
            count += len(oList) if len(oList) > diff else offset
        iList = []
        print('oList: ', oList)
        for i in range(offset):
            iList.append(oList.pop())
        iList.reverse()
        oList.append(iList)

    def getParanOffset(self, parsedInput, index, balanced=0):
        offset = index - 1
        balanced = balanced
        parenOffset = False
        count = 0

        while(True):
            currentValue = str(parsedInput[offset])
            if (re.match(self.paranPattern[0], currentValue)):
                parenOffset = False
                if (balanced == 0 or
                        len(currentValue) > balanced):
                    break
                else:
                    balanced -= len(currentValue)
            elif (re.match(self.paranPattern[1], currentValue)):
                balanced += len(currentValue)
                if not parenOffset:
                    parenOffset = True
                    count += 1
            if not parenOffset:
                count += 1
            offset -= 1
            continue
        return count

    def parseInput(self):
        return list(filter(lambda x: not re.match('^\\s*$', x),
                           re.split(self.inputMatch, self.rawInput)))

    def invalidNegativeNumbers(rawInput):
        invalidPattern = '(?:^|[^0-9).])(-[0-9.]{1,})[^\)0-9.]{1}'
        invalids = list(map(lambda i: i[1],
                            re.findall(invalidPattern, rawInput)))
        return '' if len(invalids) == 0 else 'Input Error: \
        {0} - Negative numbers expected to be wrapped in parentheses.'\
        .format(invalids)

    def invalidCharacters(rawInput):
        ops = ''.join([r'\{0}'.format(op)
                       for op in Calculator.supportedOperators])
        invalidPattern = '[^0-9\.()'+ops+']{1,}'
        invalids = re.findall(invalidPattern, rawInput)
        return '' if len(invalids) == 0 else 'Input Error: \
        {0} - Invalid input found.'.format(invalids)

    def duplicateOperators(rawInput):
        ops = ''.join([r'\{0}'.format(op)
                       for op in Calculator.supportedOperators])
        invalidPattern = '['+ops+']{2,}'
        invalids = re.findall(invalidPattern, rawInput)

        return '' if len(invalids) == 0 else 'Input Error: \
        {0} - Invalid operator usage found.'.format(invalids)

    def balancedParentheses(rawInput):
        oParenCount = re.findall(Calculator.paranPattern[0], rawInput)
        cParenCount = re.findall(Calculator.paranPattern[1], rawInput)
        balanced = len(oParenCount) == len(cParenCount)

        return '' if balanced else 'Input Error: \
        Parentheses must be balanced.'

    def validateInput(rawInput):
        """Returns dictionary of input errors with preformatted messages\
        , if any errors occured."""
        this = Calculator

        return {
            'invalidNegativeNumbers': this.invalidNegativeNumbers(rawInput),
            'invalidCharacters': this.invalidCharacters(rawInput),
            'invalidOperators': this.duplicateOperators(rawInput),
            'invalidParentheses': this.balancedParentheses(rawInput)
            # 'invalidFormat': this.invalidFormat(rawInput)
        }

    def calculate(self, x, op, y):
        operatorFunctions = {
            '^': self.power,
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide
        }
        return operatorFunctions[op](x, y)

    def evaluate(self, x, op, y):
        X = x
        Y = y

        if isinstance(x, list):
            X = self.evaluate(x[0], x[1], x[2])
        if isinstance(y, list):
            Y = self.evaluate(y[0], y[1], y[2])
        if not re.match(self.operatorMatch, op):
            print('ERROR - Expected operator, got: {0}'.format(op))
            return None

        return self.calculate(X, op, Y)

    def formatInput(self):
        debug = self.debug
        parsedInput = self.parsedInput
        index = 0
        previousOp = ''
        nestedCounter = 0
        statements = []

        if debug:
            print(statements)

        while (index < len(parsedInput)):
            lastVal = parsedInput[index - 1] if index != 0 else None
            value = parsedInput[index]
            nextVal = parsedInput[index + 1] \
                if index + 1 != len(parsedInput) else None

            if debug:
                print('PREVIOUS STATE: ', statements)
                print(value)

            # End of ParsedInput Test
            if (value == '='):
                crawlIndex = index - 1
                while(isinstance(parsedInput[crawlIndex], str) and
                        re.match(self.characterMatch,
                                 parsedInput[crawlIndex])):
                    crawlIndex -= 1
                sList = statements
                while (True):
                    if(isinstance(sList[len(sList) - 1], list)):
                        sList = sList[len(sList) - 1]
                    else:
                        break
                sList.append(decimal.Decimal(parsedInput[crawlIndex]))

                index += 1
                continue

            # Negative Number Test
            if (isinstance(lastVal, str) and value == '-'):
                if (re.match(self.paranPattern[0], lastVal)):
                    if debug:
                        print('Old State: ', parsedInput)

                    parsedInput[index] = decimal.Decimal('-' + nextVal)

                    # Ahead mutated first to reduce impact on lookbehind
                    self.handleMultiParan(parsedInput, index + 2, ')')
                    # Remove Num Val ahead
                    parsedInput.pop(index + 1)
                    # Mutated lookbehind, we must modify index if pop
                    index -= self.handleMultiParan(parsedInput,
                                                   index - 1, '(')
                    if debug:
                        print('New State: ', parsedInput)

                    nestedCounter -= 1
                    index += 1
                    continue

            # Value == '('
            if (re.match(self.paranPattern[0], value)):
                if self.debug:
                    print('oParen: Incrementing by {0}'.format(len(value)))
                nestedCounter += len(value)

                # Handle Natural Multiplication Statement
                if (re.search(self.numberMatch, str(lastVal))):
                    parenLength = len(value)
                    parsedInput[index] = '*'
                    parsedInput.insert(index + 1, '(' * parenLength)
                    print('Merge Func:')
                    print(parsedInput)

                    # Jump back an index to handle the multiplication operation
                    index -= 1
                    continue
                index += 1
                continue
            # Value == ')'
            if (re.match(self.paranPattern[1], value)):
                cParen = len(value)
                if self.debug:
                    print('cParen: Decrementing by {0}'.format(cParen))
                nestedCounter -= cParen

                # Case 1: Handle Natural Mulitplication (None returning)
                if (isinstance(nextVal, str) and
                    (re.match(self.paranPattern[0], nextVal) or
                     re.match(self.numberMatch, nextVal))):
                    parsedInput.insert(index + 1, '*')

                # Case 2: Parenthesis Enclose single statement
                if (re.search(self.numberMatch, str(lastVal))):
                    if (re.match(self.paranPattern[0],
                                 parsedInput[index - 2])):
                        print('Before Paren Change: ', parsedInput)
                        index -= self.handleMultiParan(parsedInput, index,
                                                       self.paranPattern[1])
                        index -= self.handleMultiParan(parsedInput, index - 1,
                                                       self.paranPattern[0])
                        print('After Paren Change: ', parsedInput,
                              ' index: ', index)

                        index += 1
                        continue

                # Case 3: Handle Presedence of Parentheses
                pIndex = 0
                while (pIndex < cParen):
                    if debug:
                        print('Raised Presedence:')
                        print(' -- Before -- ')
                        print(statements)

                    if (pIndex > 0):
                        fixedIndex = index - 2
                    else:
                        fixedIndex = index - 1

                    cOffset = self.getParanOffset(parsedInput,
                                                  fixedIndex, pIndex)
                    print('Offset: ', str(cOffset))
                    print(len(statements) - cOffset)
                    self.raisePresedence(statements, cOffset)

                    if debug:
                        print(' -- After -- ')
                        print(statements)
                    pIndex += 1
                index += 1
                continue
            # Value == Operator
            if (re.match(self.operatorMatch, value)):
                # Order OPs
                if (previousOp != '' and self.orderOfOperations[value]
                        <= self.orderOfOperations[previousOp]):
                    if debug:
                        print('Order Ops: ', statements)
                        print('{0} > {1}'.format(value, previousOp))

                    crawlIndex = index - 1
                    while(isinstance(parsedInput[crawlIndex], str)
                            and re.match(self.characterMatch,
                                         parsedInput[crawlIndex])):
                        crawlIndex -= 1
                    oList = statements
                    while (True):
                        if(isinstance(oList[len(oList) - 1],
                                      list)):
                            oList = oList[len(oList) - 1]
                        else:
                            break
                    oList.append(decimal.Decimal(
                        parsedInput[crawlIndex]))
                    # statements.append(decimal.Decimal(lastVal))
                    statements.append(value)
                    self.raisePresedence(statements)

                    if debug:
                        print('Order Ops Nested: ', statements)

                    # Should we even append if nested?
                    # if (nestedCounter == 0):
                    #     if (self.orderOfOperations[value] <
                    #             self.orderOfOperations[previousOp]):
                    #         print('Changed pOps: ', value)
                    #         previousOp = value
                    index += 1
                    continue
                # Regular statement
                # We always append last val and the operation here.
                # While len(statements) - 1 is list, we traverse the
                # list until we find the last len
                if (len(statements) == 0):
                    statements.append(decimal.Decimal(lastVal))
                elif (isinstance(statements[len(statements) - 1],
                                 list)):
                    if debug:
                        print('Nesting Value in list: ', statements)
                        print('Last Value: ', lastVal)
                    crawlIndex = index - 1
                    while(isinstance(parsedInput[crawlIndex], str)
                            and re.match(self.characterMatch,
                                         parsedInput[crawlIndex])):
                        crawlIndex -= 1
                    oList = statements
                    while (True):
                        if(isinstance(oList[len(oList) - 1],
                                      list)):
                            oList = oList[len(oList) - 1]
                        else:
                            break
                    oList.append(decimal.Decimal(
                        parsedInput[crawlIndex]))
                    if debug:
                        print(oList)
                        print('New list: ', statements)
                elif (isinstance(lastVal, str) and not
                        re.match(self.characterMatch,
                                 lastVal)):
                    statements.append(decimal.Decimal(lastVal))
                else:
                    crawlIndex = index - 1
                    while(isinstance(parsedInput[crawlIndex], str)
                            and re.match(self.characterMatch,
                                         parsedInput[crawlIndex])):
                        crawlIndex -= 1
                    statements.append(decimal.Decimal(
                        parsedInput[crawlIndex]))
                statements.append(value)
                previousOp = value if nestedCounter == 0 else previousOp
                index += 1
                continue
            index += 1
        return statements

    def parseOperations(self):
        operations = self.operations
        debug = self.debug
        answer = None
        sIndex = 0

        if debug:
            print(operations)

        while (sIndex < len(operations)):
            if isinstance(operations[sIndex], list):
                x = operations[sIndex][0]
                op = operations[sIndex][1]
                y = operations[sIndex][2]
                sIndex += 1
            elif (isinstance(operations[sIndex], str) and
                  re.match(self.operatorMatch, operations[sIndex])):
                x = answer
                op = operations[sIndex]
                y = operations[sIndex + 1]
                sIndex += 2
            else:
                x = operations[sIndex]
                op = operations[sIndex + 1]
                y = operations[sIndex + 2]
                sIndex += 3
            print('Evaluating: ', x, op, y)
            evalAns = self.evaluate(x, op, y)
            if debug:
                print('-> ', evalAns)
            if evalAns is not None:
                answer = decimal.Decimal(evalAns)
            else:
                if debug:
                    print(operations)
                print('ERR: Failed to calculate')
                break
        return answer

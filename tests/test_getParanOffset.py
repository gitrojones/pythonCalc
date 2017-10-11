from calculator import Calculator

calc = Calculator('(5+((5*6)/3)-(3*4))/2=', debug=True, precision=4)
parsedInput = calc.parsedInput


class TestGetParanOffset(object):
    def test_simpleNest(self):
        index = len(parsedInput) - 4
        print(parsedInput)

        offsets = []
        cParen = len(parsedInput[index])
        pIndex = 0
        while (pIndex < cParen):
            offsets.append(calc.getParanOffset(parsedInput, index - 1, pIndex))
            pIndex += 1

        assert offsets == [12, 0]

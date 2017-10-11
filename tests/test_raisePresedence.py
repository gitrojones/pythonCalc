from calculator import Calculator


class TestRaisePresedence(object):
    def test_operator(self):
        operations = [5, '+', -3, '*']
        Calculator.raisePresedence(operations, 2)
        assert operations == [5, '+', [-3, '*']]

    def test_nestedOperator(self):
        operations = [6, '-', [5, '+', -3, '*']]
        Calculator.raisePresedence(operations, 2)
        assert operations == [6, '-', [5, '+', [-3, '*']]]

    def test_deepNestedOperator(self):
        operations = [6, '-', [3, '-', [5, '+', -3], '+', 4, '*']]
        Calculator.raisePresedence(operations, 2)
        assert operations == [6, '-', [3, '-', [5, '+', -3], '+', [4, '*']]]

from calculator import Calculator
import decimal

precision = 4
decimal.getcontext().prec = precision
calc = Calculator(debug=True, precision=precision)


class TestMathStatements(object):
    def test_addition(self):
        assert calc('5+5=') == decimal.Decimal('10.0')
        assert calc('5.25+2=') == decimal.Decimal('7.25')
        assert calc('0.11+0.14=') == decimal.Decimal('0.25')
        assert calc('(5+5)=') == decimal.Decimal('10.0')
        assert calc('(5+(-5))=') == decimal.Decimal('0.0')
        assert calc('(-5.25)+(-25)=') == decimal.Decimal('-30.25')
        assert calc('((-5)+(-.5))=') == decimal.Decimal('-5.5')

    def test_subtraction(self):
        assert calc('5-5=') == decimal.Decimal('0.0')
        assert calc('5.25-2=') == decimal.Decimal('3.25')
        assert calc('0.20-0.15=') == decimal.Decimal('0.05')
        assert calc('(5-5)=') == decimal.Decimal('0.0')
        assert calc('(5-(-5))=') == decimal.Decimal('10.0')
        assert calc('(-5.25)-(-25)=') == decimal.Decimal('19.75')
        assert calc('((-5)-(-.5))=') == decimal.Decimal('-4.50')

    def test_multiply(self):
        assert calc('5*5=') == decimal.Decimal('25.0')
        assert calc('5.25*2=') == decimal.Decimal('10.5')
        assert calc('0.20*0.15=') == decimal.Decimal('0.03')
        assert calc('(5*5)=') == decimal.Decimal('25.0')
        assert calc('(5*(-5))=') == decimal.Decimal('-25.0')
        assert calc('(-5.25)*(-25)=') == decimal.Decimal('131.2')
        assert calc('((-5)*(-.5))=') == decimal.Decimal('2.5')
        assert calc('(5)(3)=') == decimal.Decimal('15.0')
        assert calc('((-5))(3)=') == decimal.Decimal('-15.0')
        assert calc('5((-3))=') == decimal.Decimal('-15.0')
        assert calc('((-3))5=') == decimal.Decimal('-15.0')
        assert calc('5*0=') == decimal.Decimal('0.0')

    def test_divide(self):
        assert calc('5/5=') == decimal.Decimal('1.0')
        assert calc('5.25/2=') == decimal.Decimal('2.625')
        assert calc('0.20/0.15=') == decimal.Decimal('1.333')
        assert calc('(5/5)=') == decimal.Decimal('1.0')
        assert calc('(5/(-5))=') == decimal.Decimal('-1.0')
        assert calc('(-5.25)/(-25)=') == decimal.Decimal('0.21')
        assert calc('((-5)/(-.5))=') == decimal.Decimal('10.0')

    def test_pow(self):
        assert calc('5^5=') == decimal.Decimal('3125')
        assert calc('5.25^2=') == decimal.Decimal('27.56')
        assert calc('0.20^0.15=') == decimal.Decimal('0.7855')
        assert calc('(5^5)=') == decimal.Decimal('3125')
        assert calc('(5^(-5))=') == decimal.Decimal('0.00032')
        assert calc('(-5.25)^(-2)=') == decimal.Decimal('0.03628')
        assert calc('((-5)^(-5))=') == decimal.Decimal('-0.00032')

    def test_oop(self):
        assert calc('(5+3)(3-2)=') == decimal.Decimal('8.0')
        assert calc('5(3+2)=') == decimal.Decimal('25.0')
        assert calc('(3-1)5=') == decimal.Decimal('10.0')
        # assert calc('1-4+2-6/3+9*2=') == decimal.Decimal('-25.0')
        assert calc('((1+1)*2)/3=') == decimal.Decimal('1.333')
        assert calc('(((-1)+3)*2)/4=') == decimal.Decimal('1.0')
        assert calc('(((5*5)))/3=') == decimal.Decimal('8.333')

    def test_mathaids(self):
        # Fails, needs to nest operations rather than return answer here.
        # TODO: Fix this condition, at a later point...
        assert calc('5+2-1*13=') == decimal.Decimal('-6')
        assert calc('12-18/2*15=') == decimal.Decimal('-123')
        assert calc('12*13-15/3=') == decimal.Decimal('151')
        assert calc('7-2+20/2=') == decimal.Decimal('-5')
        assert calc('15/3-2*4=') == decimal.Decimal('-3')

import operator

class Operable:
    def __add__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.add, other)

    def __radd__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.add, other)

    def __sub__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.sub, other)

    def __rsub__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.sub, other)

    def __mul__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.mul, other)

    def __rmul__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.mul, other)

    def __truediv__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.truediv, other)

    def __rtruediv__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.truediv, other)

    def __floordiv__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.floordiv, other)

    def __rfloordiv__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.floordiv, other)

    def __pow__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.pow, other)

    def __rpow__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.pow, other)

    def __mod__(self, other):
        from .operator import BinaryOperator
        return BinaryOperator(self, operator.mod, other)

    def __rmod__(self, other):
        from .operator import RBinaryOperator
        return RBinaryOperator(self, operator.mod, other)

    def __pos__(self):
        from .operator import UnaryOperator
        return UnaryOperator(self, operator.pos)

    def __neg__(self):
        from .operator import UnaryOperator
        return UnaryOperator(self, operator.neg)


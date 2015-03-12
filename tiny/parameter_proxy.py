import operator

class ParameterProxy:
    def __init__(self, value=0):
        self.parameters = []
        self.operator = None
        self._value = value

    @property
    def value(self):
        if self.operator and self._value is not None:
            return self.operator(self._value)
        return self._value

    def __rrshift__(self, other):
        self._value = other
        for parameter in self.parameters:
            self.value >> parameter

    def __mul__(self, other):
        self.operator = ParameterOperator(self.operator, other, operator.mul)
        return self

class ParameterOperator:
    def __init__(self, child, other, operator):
        self.child = child
        self.other = other
        self.operator = operator

    def __call__(self, value):
        if self.child is not None:
            value = self.child(value)
        return self.operator(value, self.other)


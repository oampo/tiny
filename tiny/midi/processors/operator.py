from .operable import Operable
from .filterable import Filterable

class BinaryOperator(Operable, Filterable):
    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def __call__(self, message):
        return self.operator(self.attribute(message), self.value)

class RBinaryOperator(Operable, Filterable):
    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def __call__(self, message):
        return self.operator(self.value, self.attribute(message))

class UnaryOperator(Operable, Filterable):
    def __init__(self, attribute, operator):
        self.operator = operator
        self.attribute = attribute

    def __call__(self, message):
        return self.operator(self.attribute(message))

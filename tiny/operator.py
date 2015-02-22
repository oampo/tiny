from .unit import Unit
from .rate import Rate

class Operator(Unit):
    def __init__(self, left, right, operator):
        super(Operator, self).__init__(0, right.output_channels)

        self.left = left
        self.right = right
        self.operator = operator

    def count(self):
        return self.left.count() + self.right.count() + 1

    def count_units(self):
        return self.left.count_units() + self.right.count_units()

    def acquire(self, expression_id, unit_id):
        self.left.acquire(expression_id, unit_id)
        unit_id += self.left.count_units()
        self.right.acquire(expression_id, unit_id)

    def expression(self, byte_code):
        self.left.expression(byte_code)
        self.right.expression(byte_code)
        byte_code += [self.operator, self.output_channels, Rate.audio]

    def set_parameters(self, byte_code):
        self.left.set_parameters(byte_code)
        self.right.set_parameters(byte_code)

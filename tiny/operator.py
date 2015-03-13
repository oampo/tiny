from .unit import Unit


class Operator(Unit):
    def __init__(self, left, right, operator, rate):
        super(Operator, self).__init__(0, right.output_channels, rate, rate)
        self._left = left
        self._right = right
        self._operator = operator

    def count(self):
        return self._left.count() + self._right.count() + 1

    def count_units(self):
        return self._left.count_units() + self._right.count_units()

    def realize(self, expression_id, unit_id):
        self._left.realize(expression_id, unit_id)
        unit_id += self._left.count_units()
        self._right.realize(expression_id, unit_id)

    def expression(self, byte_code):
        self._left.expression(byte_code)
        self._right.expression(byte_code)
        byte_code += [self._operator, self.output_channels, self.output_rate]

    def set_parameters(self, byte_code):
        self._left.set_parameters(byte_code)
        self._right.set_parameters(byte_code)

    def __getattr__(self, attribute):
        try:
            return getattr(object.__getattribute__(self, "_left"), attribute)
        except AttributeError:
            return getattr(object.__getattribute__(self, "_right"), attribute)

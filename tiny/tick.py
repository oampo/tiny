from . import unit


class Tick(unit.Unit):
    def __init__(self, left, right):
        super(Tick, self).__init__(0, right.output_channels, left.input_rate,
                                   right.output_rate)

        self._left = left
        self._right = right

    def count(self):
        return self._left.count() + self._right.count()

    def count_units(self):
        return self._left.count_units() + self._right.count_units()

    def realize(self, expression_id, unit_id):
        self._left.realize(expression_id, unit_id)
        unit_id += self._left.count_units()
        self._right.realize(expression_id, unit_id)

    def expression(self, byte_code):
        self._left.expression(byte_code)
        self._right.expression(byte_code)

    def set_parameters(self, byte_code):
        self._left.set_parameters(byte_code)
        self._right.set_parameters(byte_code)

    def __getattr__(self, attribute):
        try:
            return getattr(self._left, attribute)
        except AttributeError:
            return getattr(self._right, attribute)


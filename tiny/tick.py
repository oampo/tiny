from . import unit

class Tick(unit.Unit):
    def __init__(self, left, right):
        super(Tick, self).__init__(0, right.output_channels)

        self.left = left
        self.right = right

    def count(self):
        return self.left.count() + self.right.count()

    def acquire(self, expression_id, unit_id):
        if isinstance(self.left, unit.Unit):
            self.left.acquire(expression_id, unit_id)
        if isinstance(self.right, unit.Unit):
            self.right.acquire(expression_id, unit_id + 1)

    def expression(self, byte_code):
        self.left.expression(byte_code)
        self.right.expression(byte_code)

    def set_parameters(self, byte_code):
        self.left.set_parameters(byte_code)
        self.right.set_parameters(byte_code)

import .unit

class Operator(Unit):
    def __init__(self, left, right, operator):
        super(Tick, self).__init__(0, right.output_channels)

        self.left = left
        self.right = right
        self.operator = operator

    def count(self):
        return self.left.count() + self.right.count()

    def acquire(self, expression):
        self.left.acquire(expression)
        self.right.acquire(expression)

    def expression(self, byte_code):
        self.left.expression(byte_code)
        self.right.expression(byte_code)

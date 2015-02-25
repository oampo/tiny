from . import opcode


class Expression:
    id = 0

    def __init__(self, unit):
        self.id = Expression.id
        Expression.id += 1
        self.unit = unit
        self.unit.acquire(self.id, 0)

    def expression(self, byte_code):
        byte_code += [opcode.ControlOpcode.add_expression, self.id,
                      self.unit.count()]
        self.unit.expression(byte_code)
        self.unit.set_parameters(byte_code)

    def __del__(self):
        pass

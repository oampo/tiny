from . import opcode


class Expression:
    id = 0

    def __init__(self, unit):
        self.id = Expression.id
        Expression.id += 1
        self._unit = unit
        self._unit.realize(self.id, 0)

    def expression(self, byte_code):
        byte_code += [opcode.ControlOpcode.add_expression, self.id,
                      self._unit.count()]
        self._unit.expression(byte_code)
        self._unit.set_parameters(byte_code)

    def remove(self):
        pass

    def __getattr__(self, attribute):
        return getattr(self._unit, attribute)

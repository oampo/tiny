from .opcode import ControlOpcode


class Expression:
    id = 0

    def __init__(self, unit):
        self.id = Expression.id
        Expression.id += 1
        self._unit = unit
        self._unit.realize(self.id, 0)

    def expression(self, byte_code):
        byte_code += [ControlOpcode.add_expression, self.id,
                      self._unit.count()]
        self._unit.expression(byte_code)
        self._unit.set_parameters(byte_code)

    def remove(self, byte_code=None):
        from .server import server
        send = False

        if not byte_code:
            byte_code = []
            send = True

        byte_code += [ControlOpcode.remove_expression, self.id]

        if send:
            server.send(byte_code)

    def __getattr__(self, attribute):
        return getattr(self._unit, attribute)

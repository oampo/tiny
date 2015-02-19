import numbers

from . import opcode
from . import unit

class Parameter:
    def __init__(self, value=0):
        self.expression_id = None
        self.unit_id = None
        self.id = None
        self.value = value

    def acquire(self, expression_id, unit_id, parameter_id):
        print(expression_id, unit_id, parameter_id)
        self.expression_id = expression_id
        self.unit_id = unit_id
        self.id = parameter_id

    def expression(self, byte_code):
        byte_code += [opcode.DspOpcode.parameter, self.expression_id,
                      self.unit_id, self.id]

    def set_parameter(self, byte_code):
        byte_code += [opcode.ControlOpcode.set_parameter, self.expression_id,
                      self.unit_id, self.id, float(self.value)]

    def _tick_in_unit(self, unit):
        if other.output_channels != 1:
            raise ChannelMismatchError()
        return tick.Tick(other, self)

    def _tick_in_number(self, number):
        from . import server
        self.value = number
        self >> server.server

    def __rrshift__(self, other):
        if isinstance(other, unit.Unit):
            return self._tick_in_unit(other)
        elif isinstance(other, numbers.Number):
            return self._tick_in_number(other)
        elif isinstance(other, collections.Iterable):
            pass
        return NotImplemented


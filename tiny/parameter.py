import numbers

from . import opcode
from . import unit
from . import tick

class Parameter:
    def __init__(self, value=0):
        self.expression_id = None
        self.unit_id = None
        self.id = None
        self.value = value
        self.input_channels = 1
        self.output_channels = 0

    def acquire(self, expression_id, unit_id, parameter_id):
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
        from . import server
        from .units import ParameterWriterAr
        if unit.output_channels != 1:
            raise ChannelMismatchError()
        writer = ParameterWriterAr(self.expression_id, self.unit_id, self.id)
        expression = tick.Tick(unit, writer) >> server.server
        server.server.add_edge(expression.id, self.expression_id)
        return expression

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


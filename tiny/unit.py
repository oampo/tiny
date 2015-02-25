import numbers
from inspect import Parameter, Signature

from .opcode import DspOpcode
from .errors import ChannelMismatchError
from .rate import Rate

class Unit:
    definition = {
    }

    def __init__(self, input_channels, output_channels, input_rate,
                 output_rate):
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.input_rate = input_rate
        self.output_rate = output_rate
        self.parameters = []
        self.expression_id = None

    def count(self):
        return 1

    def count_units(self):
        return 1

    def acquire(self, expression_id, unit_id):
        self.expression_id = expression_id
        self.id = unit_id

        for parameter_id, parameter in enumerate(self.parameters):
            parameter.acquire(expression_id, unit_id, parameter_id)

    def expression(self, byte_code):
        byte_code += [DspOpcode.unit, self.id,
                      self.definition["type_id"], self.input_channels,
                      self.output_channels]

    def set_parameters(self, byte_code):
        for parameter in self.parameters:
            parameter.set_parameter(byte_code)

    def _tick_in_unit(self, unit):
        from . import tick
        if self.input_channels != unit.output_channels:
            raise errors.ChannelMismatchError(self.input_channels,
                                              unit.output_channels)
        return tick.Tick(unit, self)

    def _operate_unit(self, unit, opcode):
        from .operator import Operator
        if self.output_channels != unit.output_channels:
            raise ChannelMismatchError(self.output_channels,
                                       unit.input_channels)

        if (self.output_rate == Rate.control and
                unit.output_rate == Rate.audio):
            return Operator(self >> KrToAr(), unit, opcode, Rate.audio)
        elif (self.output_rate == Rate.audio and
                unit.output_rate == Rate.control):
            return Operator(self, unit >> KrToAr(), opcode, Rate.audio)
        else:
            return Operator(self, unit, opcode, self.output_rate)

    def _operate_number(self, number, opcode):
        from .units import ParameterAr, ParameterKr
        from .operator import Operator
        if self.definition.rate == Rate.audio:
            parameter = ParameterAr(number, channels=self.output_channels)
        elif self.definition.rate == Rate.control:
            parameter = ParameterKr(number, channels=self.output_channels)
        return Operator(self, parameter, opcode)

    def __rrshift__(self, other):
        if isinstance(other, Unit):
            return self._tick_in_unit(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Unit):
            return self._operate_unit(other, DspOpcode.add)
        elif isinstance(other, numbers.Number):
            return self._operate_number(other, DspOpcode.add)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Unit):
            return self._operate_unit(other, DspOpcode.multiply)
        elif isinstance(other, numbers.Number):
            return self._operate_number(other, DspOpcode.multiply)
        return NotImplemented


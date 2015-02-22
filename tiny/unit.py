import numbers
from inspect import Parameter, Signature

from . import opcode
from . import errors
from . import util

class Unit:
    definition = {
    }

    def __init__(self, input_channels, output_channels):
        self.input_channels = input_channels
        self.output_channels = output_channels
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
        byte_code += [opcode.DspOpcode.unit, self.id,
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

    def _add_unit(self, unit):
        from .operator import Operator
        if self.output_channels != unit.output_channels:
            raise errors.ChannelMismatchError(self.output_channels,
                                              unit.input_channels)
        return Operator(self, unit, opcode.DspOpcode.add)

    def _multiply_unit(self, unit):
        from .operator import Operator
        if self.output_channels != unit.output_channels:
            raise errors.ChannelMismatchError(self.output_channels,
                                              unit.input_channels)
        return Operator(self, unit, opcode.DspOpcode.multiply)

    def _add_number(self, number):
        from .units import ParameterAr
        from .operator import Operator
        parameter = ParameterAr(number, channels=self.output_channels)
        return Operator(self, parameter, opcode.DspOpcode.add)

    def _multiply_number(self, number):
        from .units import ParameterAr
        from .operator import Operator
        parameter = ParameterAr(number, channels=self.output_channels)
        return Operator(self, parameter, opcode.DspOpcode.multiply)

    def __rrshift__(self, other):
        if isinstance(other, Unit):
            return self._tick_in_unit(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Unit):
            return self._add_unit(other)
        elif isinstance(other, numbers.Number):
            return self._add_number(other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Unit):
            return self._multiply_unit(other)
        elif isinstance(other, numbers.Number):
            return self._multiply_number(other)
        return NotImplemented


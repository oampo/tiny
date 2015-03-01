import numbers
import collections

from . import unit
from . import tick
from .errors import ChannelMismatchError
from .rate import Rate
from .opcode import ControlOpcode
from .expression import Expression


class Parameter:
    def __init__(self, value=0):
        self.expression_id = None
        self.unit_id = None
        self.id = None

        self.realized = False

        self.value = value
        self.input_channels = 1
        self.output_channels = 0

        self.controlled = False
        self.controller = None
        self.controller_expression = None

    def realize(self, expression_id, unit_id, parameter_id):
        self.expression_id = expression_id
        self.unit_id = unit_id
        self.id = parameter_id

        self.realized = True

    def unrealize(self):
        self.expression_id = None
        self.unit_id = None
        self.id = None

        self.realized = False

    def set_parameter(self, byte_code):
        byte_code += [ControlOpcode.set_parameter, self.expression_id,
                      self.unit_id, self.id, float(self.value)]
        if self.controlled:
            self._run_controller(byte_code)

    def _run_controller(self, byte_code):
        from .units import ParameterWriterAr, ParameterWriterKr
        if self.controller.output_rate == Rate.audio:
            writer = ParameterWriterAr(self.expression_id, self.unit_id,
                                       self.id)
        elif self.controller.output_rate == Rate.control:
            writer = ParameterWriterKr(self.expression_id, self.unit_id,
                                       self.id)

        self.controller_expression = Expression(self.controller >> writer)
        self.controller_expression.expression(byte_code)

        byte_code += [ControlOpcode.add_edge, self.controller_expression.id,
                      self.expression_id]

    def _tick_in_unit(self, unit):
        from .server import server
        self.controller = unit
        self.controlled = True

        if self.realized:
            byte_code = []
            self._run_controller(byte_code)
            server.send(byte_code)

    def _tick_in_number(self, number):
        from .server import server
        self.value = number

        self.controller = None
        self.controlled = False

        if self.realized:
            if self.controlled:
                self.controller_expression.remove()
                self.controller_expression = None

            self >> server

    def __rrshift__(self, other):
        if isinstance(other, unit.Unit):
            return self._tick_in_unit(other)
        elif isinstance(other, numbers.Number):
            return self._tick_in_number(other)
        elif isinstance(other, collections.Iterable):
            pass
        return NotImplemented

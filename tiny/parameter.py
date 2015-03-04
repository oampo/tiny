import numbers
import collections

from . import unit
from . import tick
from .errors import ChannelMismatchError
from .rate import Rate
from .opcode import ControlOpcode
from .expression import Expression
from .parameter_proxy import ParameterProxy


class Parameter:
    def __init__(self, value=0):
        self.expression_id = None
        self.unit_id = None
        self.id = None

        self.realized = False

        self.input_channels = 1
        self.output_channels = 0

        self.controlled = False
        self._controller = None
        self._controller_expression = None

        self.value = 0
        value >> self

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
        if self._controller.output_rate == Rate.audio:
            writer = ParameterWriterAr(self.expression_id, self.unit_id,
                                       self.id)
        elif self._controller.output_rate == Rate.control:
            writer = ParameterWriterKr(self.expression_id, self.unit_id,
                                       self.id)

        self._controller_expression = Expression(self._controller >> writer)
        self._controller_expression.expression(byte_code)

        byte_code += [ControlOpcode.add_edge, self._controller_expression.id,
                      self.expression_id]

    def _tick_in_unit(self, unit):
        from .server import server
        self._controller = unit
        self.controlled = True

        if self.realized:
            if self.controlled:
                self._controller_expression.remove()
                self._controller_expression = None
            byte_code = []
            self._run_controller(byte_code)
            server.send(byte_code)

    def _tick_in_number(self, number):
        from .server import server
        self.value = number

        self._controller = None
        self.controlled = False

        if self.realized:
            if self.controlled:
                self._controller_expression.remove()
                self._controller_expression = None

            self >> server

    def _tick_in_proxy(self, proxy):
        proxy.parameters.append(self)
        proxy.value >> self

    def __rrshift__(self, other):
        if isinstance(other, unit.Unit):
            return self._tick_in_unit(other)
        elif isinstance(other, numbers.Number):
            return self._tick_in_number(other)
        elif isinstance(other, ParameterProxy):
            return self._tick_in_proxy(other)
        elif isinstance(other, collections.Iterable):
            pass
        return NotImplemented

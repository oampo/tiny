import struct
import socket

from .unit import Unit
from .expression import Expression
from .parameter import Parameter
from .opcode import ControlOpcode


class Server:
    def __init__(self, host="127.0.0.1", port=42753):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, byte_code):
        print(byte_code)
        packed = bytes()
        for opcode in byte_code:
            if isinstance(opcode, int):
                packed = packed + struct.pack(">I", opcode)
            elif isinstance(opcode, float):
                packed = packed + struct.pack(">f", opcode)
        self.socket.sendto(packed, (self.host, self.port))

    def _tick_in_unit(self, unit):
        expression = Expression(unit)
        byte_code = []
        expression.expression(byte_code)
        self.send(byte_code)
        return expression

    def _tick_in_parameter(self, parameter):
        byte_code = []
        parameter.set_parameter(byte_code)
        self.send(byte_code)

    def __rrshift__(self, other):
        if isinstance(other, Unit):
            return self._tick_in_unit(other)
        elif isinstance(other, Parameter):
            return self._tick_in_parameter(other)
        return NotImplemented

server = Server()

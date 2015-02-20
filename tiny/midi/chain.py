from ..parameter import Parameter
from .processors import set_parameter

class MidiChain:
    def __init__(self):
        self.chain = []

    def run(self, message):
        for processor in self.chain:
            if message is None:
                break

            message = processor(message)

    def _chain_callable(self, callable):
        self.chain.append(callable)

    def _chain_parameter(self, parameter):
        self.chain.append(set_parameter(parameter))


    def __rshift__(self, other):
        if callable(other):
            return self._chain_callable(other)
        elif isinstance(other, Parameter):
            return self._chain_parameter(other)

        return NotImplemented
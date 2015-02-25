from ..parameter import Parameter


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
        return self

    def _chain_parameter(self, parameter):
        from .processors import SetParameter
        self.chain.append(SetParameter(parameter))

    def __rshift__(self, other):
        if callable(other):
            return self._chain_callable(other)
        elif isinstance(other, Parameter):
            return self._chain_parameter(other)
        return NotImplemented

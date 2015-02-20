import traceback

import mido

from .chain import MidiChain

class MidiInput:
    def __init__(self, name):
        self.port = mido.open_input(name, callback=self.on_message)

        self.chains = []

    def on_message(self, message):
        for chain in self.chains[:]:
            try:
                chain.run(message)
            except Exception as e:
                traceback.print_exc()
                self.chains.remove(chain)

    def __rshift__(self, other):
        if callable(other):
            chain = MidiChain()
            chain.chain.append(other)
            self.chains.append(chain)
            return chain
        return NotImplemented


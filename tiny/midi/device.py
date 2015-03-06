import traceback
import asyncio

import mido

from .chain import MidiChain


class MidiInput:
    def __init__(self, name):
        self.port = mido.open_input(name)

        self.chains = []
        asyncio.async(self._run())

    @asyncio.coroutine
    def _run(self):
        while True:
            future = loop.run_in_executor(None, self.port.receive)
            message = yield from future
            self._on_message(message)

    def _on_message(self, message):
        for chain in self.chains[:]:
            try:
                chain.run(message)
            except Exception:
                traceback.print_exc()
                self.chains.remove(chain)

    def __rshift__(self, other):
        if callable(other):
            chain = MidiChain()
            chain.chain.append(other)
            self.chains.append(chain)
            return chain
        return NotImplemented

if __name__ == "__main__":
    from .. import main
    from .processors import *

    beatstep = MidiInput("Arturia BeatStep MIDI 1")
    beatstep >> (lambda m: print(m))

    main()

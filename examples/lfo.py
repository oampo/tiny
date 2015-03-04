from tiny.server import server
from tiny.units import SineAr, SineKr, Dac, ParameterKr
from tiny.midi.device import MidiInput
from tiny.midi.processors import *
from tiny.util import unit

@unit
def synth(frequency, rate, depth=110):
    lfo = SineKr(rate) * depth + frequency
    return SineAr(frequency=lfo, channels=2)

expression = synth(220, 0.5) >> Dac() >> server

beatstep = MidiInput("Arturia BeatStep MIDI 1")
beatstep >> control_change(0, 10) >> value() * 5 >> expression.depth
beatstep >> control_change(0, 74) >> value() / 8 >> expression.frequency
beatstep >> control_change(0, 71) >> value() * 10 >> expression.rate

while 1:
    pass

from tiny.server import server
from tiny.units import SineAr, Dac, ParameterAr
from tiny.midi.device import MidiInput
from tiny.midi.processors import *

sine = SineAr(channels=2)
expression = sine >> Dac() >> server

depth = ParameterAr(110)
frequency = ParameterAr(220)
lfo = SineAr(2)
(lfo * depth + frequency) >> sine.frequency

beatstep = MidiInput("Arturia BeatStep MIDI 1")
beatstep >> control_change(0, 10) >> value() * 5 >> depth.value
beatstep >> control_change(0, 74) >> (value() / 8) >> lfo.frequency
beatstep >> control_change(0, 71) >> (value() * 10) >> frequency.value

while 1:
    pass

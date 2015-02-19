from tiny.server import server
from tiny.units import SineAr, Dac
from tiny.parameter import Parameter

expression = SineAr(channels=2) >> Dac() >> server
"""
del expression

sine = SineAr(channels=2)
dac = Dac(channels=2)

expression = sine >> dac >> server
220 >> sine.frequency
del expression

sine_a = Sine(2)
sine_b = Sine(2)
bus = Bus(2)
dac = Dac(2)

sine_a >> bus
sine_b >> bus
bus >> dac
del bus

bind = ([220, 440, 560] >> sine.frequency |
        1 >> scheduler)
del bind


bind = ([220, 440, 560] >> sine.frequency |
        [0.1, 0.5] >> sine.phase |
        [0.5, 0.2] >> scheduler)

del bind

class MySynth(Source):
    def __init__(self):
        self.sine = Sine(1)
        self.env = PercussiveEnv(1)
        self.up = UpMixer(1, 2)

        self.frequency = sine.frequency
        self.gate = env.gate

    def expression(self):
        return self.sine * self.env >> self.up

synth = MySynth()
expression = synth >> Dac() >> server
1 >> synth.gate
220 >> synth.frequency
del synth

bind = MySynth() | 1 >> scheduler
del bind

synth = MySynth()
bind = (synth |
        [220, 440, 560] >> synth.frequency |
        1 >> synth.gate |
        1 >> scheduler)
"""


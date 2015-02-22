from tiny.server import server
from tiny.units import SineAr, Dac

sine = SineAr(channels=2)
dac = Dac()

expression = sine >> dac >> server
220 >> sine.frequency


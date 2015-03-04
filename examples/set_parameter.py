from tiny.server import server
from tiny.units import SineAr, Dac

expression = SineAr(channels=2) >> Dac() >> server
220 >> expression.frequency


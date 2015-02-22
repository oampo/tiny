from tiny.server import server
from tiny.units import SineAr, Dac

SineAr(channels=2) >> Dac() >> server

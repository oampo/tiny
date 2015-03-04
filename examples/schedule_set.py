from tiny.server import server
from tiny.scheduler import Scheduler
from tiny.units import SineAr, Dac

scheduler = Scheduler()
expression = SineAr(channels=2) >> Dac() >> server

dict(
    expression=expression,
    frequency=iter([220, 440, 560]* 33),
    duration=iter([1] * 99)
) >> scheduler



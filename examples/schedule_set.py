from tiny.server import server
from tiny.scheduling.scheduler import Scheduler
from tiny.units import SineAr, Dac
from tiny import main

scheduler = Scheduler()
expression = SineAr(channels=2) >> Dac() >> server

dict(
    expression=expression,
    frequency=[220, 440, 560],
    duration=1
) >> scheduler

main()


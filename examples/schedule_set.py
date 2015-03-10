from tiny.server import server
from tiny.scheduling.scheduler import Scheduler
from tiny.units import SineAr, Dac
from tiny import main

scheduler = Scheduler()
sine = SineAr(channels=2) >> Dac() >> server

{
    sine.frequency: [220, 440, 560],
    scheduler.duration: 1
} >> scheduler

main()


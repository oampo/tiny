import time
import asyncio
import functools
from heapq import heappush, heappop

from .patterns import p_dict

class Scheduler:
    def __init__(self, bpm=120):
        self._queue = []

        self.bpm = bpm

        self._time = time.time()
        self._beat = 0
        self._beat_in_bar = 0
        self._bar = 0
        self.beats_per_bar = 4
        self._last_beat_time = self._time
        self._beat_length = 60 / bpm

        self._future = None

    def add(self, time, callback, **patterns):
        self._add(time, {"callback": callback, "patterns": p_dict(patterns)()})

    def _add(self, time, data):
        event = (time, data)
        heappush(self._queue, event)

        if self._queue[0] is event:
            self._set_timer()

    def add_relative(self, beats, callback, **patterns):
        self._update_time()
        self.add(self._time + beats * self._beat_length, callback, **patterns)

    def add_absolute(self, beat, callback, **patterns):
        self._update_time()

        time = self._last_beat_time + (beat - self._beat) * self._beat_length

        if time < self._time:
            return
        self.add(time, callback, **patterns)

    def play(self, callback, **patterns):
        self._update_time()
        process_dict = functools.partial(self._process_dict,
                                         callback=callback)
        self.add(self.time, process_dict, **patterns)

    @property
    def time(self):
        self._update_time()
        return self._time

    @property
    def beat(self):
        self._update_time()
        return self._beat

    @property
    def bar(self):
        self._update_time()
        return self._bar

    @property
    def beat_in_bar(self):
        self._update_time()
        return self._beat_in_bar

    def _update_time(self):
        self._time = time.time()

        beats_elapsed = ((self._time - self._last_beat_time) //
                         self._beat_length)
        bars_elapsed = beats_elapsed // self.beats_per_bar

        self._beat += beats_elapsed
        self._beat_in_bar = ((self._beat_in_bar + beats_elapsed) %
                             self.beats_per_bar)
        self._bar += bars_elapsed
        self._last_beat_time += beats_elapsed * self._beat_length

    def _process_events(self):
        self._update_time()
        while len(self._queue) and self._queue[0][0] <= self._time:
            event = heappop(self._queue)
            event[1]["time"] = event[0]
            self._process_event(event[1])
        self._set_timer()

    def _set_timer(self):
        if self._future != None:
            self._future.cancel()

        if not len(self._queue):
            return

        self._future = asyncio.async(self._run(self._queue[0][0]))

    @asyncio.coroutine
    def _run(self, time):
        # Uses wait strategy from threading wait
        delay = 0.0005
        while self.time < time:
            delay = min(delay * 2, time - self._time, 0.05)
            yield from asyncio.sleep(delay)
        self._process_events()

    def _process_event(self, event):
        patterns = event["patterns"]
        try:
            values = next(patterns)
        except StopIteration:
            return
        duration = event["callback"](**values)

        if duration:
            time = event.pop("time")
            self._add(time + duration * self._beat_length, event)

    def _process_dict(self, callback, **values):
        duration = values.pop("duration")
        callback(**values)
        return duration

    # Should maybe be part of expression/unit
    def _set_parameters(self, expression, **kwargs):
        for key, value in kwargs.items():
            value >> getattr(expression, key)

    def _tick_in_dict(self, dict):
        if "expression" in dict:
            expression = dict.pop("expression")
            set_parameters = functools.partial(self._set_parameters,
                                               expression)
            self.play(set_parameters, **dict)

    def __rrshift__(self, other):
        if hasattr(other, "__getitem__"):
            return self._tick_in_dict(other)
        return NotImplemented

if __name__ == "__main__":
    from .. import main
    from .patterns import p_iterable

    scheduler = Scheduler()
    scheduler.play(lambda x: print(x), x=p_iterable([1, 2, 3]) * 2, duration=1)

    main()

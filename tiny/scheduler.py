import time
import threading
import functools
from heapq import heappush, heappop

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

        self._timer = None

    def add(self, time, callback):
        self._add(time, {"callback": callback})

    def _add(self, time, data):
        event = (time, data)
        heappush(self._queue, event)

        if self._queue[0] is event:
            self._set_timer()

    def add_relative(self, beats, callback):
        self._update_time()
        self.add(self._time + beats * self._beat_length, callback)

    def add_absolute(self, beat, callback):
        self._update_time()

        time = self._last_beat_time + (beat - self._beat) * self._beat_length

        if time < self._time:
            return
        self.add(time, callback)

    def play(self, patterns, callback):
        self._update_time()
        self._add(self.time, {"patterns": patterns,
                              "callback": callback})

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
        if self._timer != None:
            self._timer.cancel()

        if not len(self._queue):
            return

        self._timer = threading.Timer(self._queue[0][0] - time.time(),
                                      self._process_events)
        self._timer.start()

    def _process_event(self, event):
        if "patterns" in event:
            patterns = event["patterns"]
            duration = patterns["duration"]
            values = {}
            for key, pattern in patterns.items():
                if key == "duration":
                    continue
                try:
                    values[key] = next(pattern)
                except StopIteration:
                    return
            event["callback"](**values)

            try:
                duration = next(duration)
            except StopIteration:
                return
            self._add(event["time"] + duration * self._beat_length,
                      {"callback": event["callback"], "patterns": patterns})
        else:
            event["callback"]()

    # Should maybe be part of expression/unit
    def _set_parameters(self, expression, **kwargs):
        for key, value in kwargs.items():
            value >> getattr(expression, key)

    def _tick_in_dict(self, dict):
        if "expression" in dict:
            expression = dict.pop("expression")
            self.play(dict, functools.partial(self._set_parameters, expression))

    def __rrshift__(self, other):
        if hasattr(other, "__getitem__"):
            return self._tick_in_dict(other)
        return NotImplemented

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.play(dict(x=iter([1, 2, 3] * 8), duration=iter([1] * 10)),
                   lambda x: print(x))

    while True:
        time.sleep(1)

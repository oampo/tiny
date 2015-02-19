class Scheduler:
    def __rrshift__(self, other):
        if isinstance(other, numbers.Number):
            return None

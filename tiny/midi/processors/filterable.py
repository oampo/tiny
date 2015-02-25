import operator

from .filter import Filter


class Filterable:
    def __lt__(self, other):
        return Filter(self, operator.lt, other)

    def __le__(self, other):
        return Filter(self, operator.le, other)

    def __eq__(self, other):
        return Filter(self, operator.eq, other)

    def __ne__(self, other):
        return Filter(self, operator.ne, other)

    def __ge__(self, other):
        return Filter(self, operator.ge, other)

    def __gt__(self, other):
        return Filter(self, operator.gt, other)

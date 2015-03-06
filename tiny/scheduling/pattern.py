import operator
import numbers


class Pattern:
    def __init__(self, generator, *args, **kwargs):
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        for value in self.generator(*self.args, **self.kwargs):
            if isinstance(value, Pattern):
                yield from value()
            else:
                yield value

    def _operate(self, other, operator):
        from .patterns import p_operate
        return p_operate(self, as_pattern(other), operator)

    def _roperate(self, other, operator):
        from .patterns import p_operate
        return p_operate(as_pattern(other), self, operator)

    def __mul__(self, other):
        return _operate(self, other, operator.mul)

    def __rmul__(self, other):
        return _roperate(self, other, operator.mul)

def pattern(generator):
    def inner(*args, **kwargs):
        return Pattern(generator, *args, **kwargs)
    return inner

def as_pattern(value):
    from .patterns import p_inf, p_list
    if isinstance(value, numbers.Number):
        return p_inf(value)
    elif isinstance(value, list):
        return p_inf(p_list(value))
    elif isinstance(value, Pattern):
        return value
    raise TypeError


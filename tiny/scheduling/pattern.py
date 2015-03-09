import operator
import numbers
import inspect


class Pattern:
    def __init__(self, generator, *args, **kwargs):
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        from .patterns import p_iterable
        for value in self.generator(*self.args, **self.kwargs):
            if isinstance(value, Pattern):
                yield from value()
            elif isinstance(value, list):
                yield from p_iterable(value)()
            else:
                yield value

    def _operate(self, other, operator):
        from .patterns import p_operate
        return p_operate(self, other, operator)

    def _roperate(self, other, operator):
        from .patterns import p_operate
        return p_operate(other, self, operator)

    def __mul__(self, other):
        return self._operate(other, operator.mul)

    def __rmul__(self, other):
        return self._roperate(other, operator.mul)

def pattern(generator):
    def inner(*args, **kwargs):
        return Pattern(generator, *args, **kwargs)
    return inner

def repeated_pattern(default_limit=None):
    from .patterns import p_repeat
    def middle(function):
        signature = inspect.signature(function)
        parameters = list(signature.parameters.values())
        limit_parameter = inspect.Parameter("limit",
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=default_limit)
        parameters.append(limit_parameter)
        signature = signature.replace(parameters=parameters)
        function = pattern(function)
        def inner(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            limit = bound.arguments.pop("limit", default_limit)
            return p_repeat(function(**bound.arguments), limit)
        return inner
    return middle

def as_pattern(value):
    from .patterns import p_value
    if isinstance(value, Pattern):
        return value
    else:
        return p_value(value)
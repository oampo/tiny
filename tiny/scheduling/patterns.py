import random

from .pattern import pattern, repeated_pattern, as_pattern


@pattern
def p_repeat(pattern, limit=1):
    count = 0
    while not limit or count < limit:
        yield pattern
        count += 1


@repeated_pattern()
def p_iterable(iterable):
    yield from iterable


@repeated_pattern()
def p_value(value):
    yield value


@repeated_pattern()
def p_random():
    yield random.random()


@repeated_pattern()
def p_choice(patterns):
    yield random.choice(patterns)


def p_inf(pattern):
    return p_repeat(pattern, None)


@pattern
def p_operate(pattern_a, pattern_b, operator):
    pattern_a = as_pattern(pattern_a)
    pattern_b = as_pattern(pattern_b)
    yield from map(lambda x, y: operator(x, y), pattern_a(), pattern_b())


@repeated_pattern(1)
def p_tuple(patterns):
    patterns = [as_pattern(pattern)() for pattern in patterns]
    yield from zip(*patterns)


@repeated_pattern(1)
def p_dict(patterns):
    patterns = {key: as_pattern(pattern)() for key, pattern in
                patterns.items()}
    while True:
        values = {key: next(pattern) for key, pattern in patterns.items()}
        yield values

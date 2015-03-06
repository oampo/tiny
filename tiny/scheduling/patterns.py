from .pattern import pattern

@pattern
def p_list(list):
    yield from list

@pattern
def p_random():
    yield random.random()

@pattern
def p_inf(pattern):
    while True:
        yield pattern

@pattern
def p_n(pattern, n):
    for _ in range(n):
        yield pattern

@pattern
def p_operate(patternA, patternB, operator):
    yield from map(lambda x, y: operator(x, y), patternA(), patternB())


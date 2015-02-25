import enum


@enum.unique
class ControlOpcode(enum.IntEnum):
    set_parameter = 0
    add_expression = 1
    add_edge = 2


@enum.unique
class DspOpcode(enum.IntEnum):
    unit = 3
    add = 4
    multiply = 5

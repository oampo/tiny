import enum


@enum.unique
class ControlOpcode(enum.IntEnum):
    set_parameter = 0
    add_expression = 1
    remove_expression = 2
    add_edge = 3


@enum.unique
class DspOpcode(enum.IntEnum):
    unit = 4
    add = 5
    multiply = 6

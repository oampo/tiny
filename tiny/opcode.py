import enum

@enum.unique
class ControlOpcode(enum.IntEnum):
    set_parameter = 0
    add_expression = 1
    play = 2

@enum.unique
class DspOpcode(enum.IntEnum):
    unit = 3
    add = 4

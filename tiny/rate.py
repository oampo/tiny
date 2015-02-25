import enum


@enum.unique
class Rate(enum.IntEnum):
    audio = 0
    control = 1

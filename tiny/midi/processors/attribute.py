from .operable import Operable
from .filterable import Filterable


class Attribute(Operable, Filterable):
    def __init__(self, attribute, types):
        self.attribute = attribute
        self.types = types

    def __call__(self, message):
        if message.type in self.types:
            return getattr(message, self.attribute)


def channel():
    return Attribute("channel", (
        "note_off", "note_on", "polytouch",  "control_change",
        "program_change", "aftertouch", "pitchwheel"
    ))


def note():
    return Attribute("note", ("note_off", "note_on"))


def velocity():
    return Attribute("velocity", ("note_off", "note_on"))


def value():
    return Attribute("value", ("polytouch", "control_change", "aftertocuh"))


def control():
    return Attribute("control", ("control_change"))


def program():
    return Attribute("program", ("program_change"))


def pitch():
    return Attribute("pitch", ("pitchwheel"))

import operator

from .filter import Filter

class Attribute:
    def __init__(self, attribute, types):
        self.attribute = attribute
        self.types = types

    def __call__(self, message):
        if message.type in self.types:
            return getattr(message, self.attribute)

    def __lt__(self, other):
        return Filter(self.attribute, self.types, operator.lt, other)

    def __le__(self, other):
        return Filter(self.attribute, self.types, operator.le, other)

    def __eq__(self, other):
        return Filter(self.attribute, self.types, operator.eq, other)

    def __ne__(self, other):
        return Filter(self.attribute, self.types, operator.ne, other)

    def __ge__(self, other):
        return Filter(self.attribute, self.types, operator.ge, other)

    def __gt__(self, other):
        return Filter(self.attribute, self.types, operator.gt, other)

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
    return Attribute("value", ("polytouch", "control_change","aftertocuh"))

def control():
    return Attribute("control", ("control_change"))

def program():
    return Attribute("program", ("program_change"))

def pitch():
    return Attribute("pitch", ("pitchwheel"))

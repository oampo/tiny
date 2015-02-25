class Type:
    def __init__(self, type, **kwargs):
        self.type = type
        self.kwargs = kwargs

    def __call__(self, message):
        if message.type == self.type:
            for attribute, value in self.kwargs.items():
                if value and getattr(message, attribute) != value:
                    return None
            return message


def note_off(channel=None, note=None, velocity=None):
    return Type("note_off", channel=channel, note=note, velocity=velocity)


def note_on(channel=None, note=None, velocity=None):
    return Type("note_on", channel=channel, note=note, velocity=velocity)


def polytouch(channel=None, note=None, value=None):
    return Type("polytouch", channel=channel, note=note, value=value)


def control_change(channel=None, control=None, value=None):
    return Type("control_change", channel=channel, control=control,
                value=value)


def program_change(channel=None, program=None):
    return Type("program_change", channel=channel, program=program)


def aftertouch(channel=None, value=None):
    return Type("aftertouch", channel=channel, value=value)


def pitchwheel(channel=None, pitch=None):
    return Type("pitchwheel", channel=channel, pitch=pitch)

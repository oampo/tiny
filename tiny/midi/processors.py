def cc(cc):
    def inner(message):
        if message.type == "control_change" and message.cc == cc:
            return message
    return inner

def value():
    def inner(message):
        if message.type in ("control_change", "aftertouch", "polytouch"):
            return message.value
    return inner

def printer():
    return lambda message: print(message)

def set_parameter(parameter):
    return lambda value: value >> parameter


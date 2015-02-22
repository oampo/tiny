class Filter:
    def __init__(self, attribute, types, operator, value):
        self.attribute = attribute
        self.types = types
        self.operator = operator
        self.value = value

    def __call__(self, message):
        if (message.type in self.types and
            self.operator(getattr(message, self.attribute), self.value)):
            return message

class Filter:
    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def __call__(self, message):
        if self.operator(self.attribute(message), self.value):
            return message

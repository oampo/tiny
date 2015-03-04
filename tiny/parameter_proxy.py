class ParameterProxy:
    def __init__(self, value=0):
        self.parameters = []
        self.value = value

    def __rrshift__(self, other):
        for parameter in self.parameters:
            other >> parameter

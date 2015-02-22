class SetParameter:
    def __init__(self, parameter):
        self.parameter = parameter

    def __call__(self, value):
        value >> self.parameter

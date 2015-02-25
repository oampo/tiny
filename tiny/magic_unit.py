from . import util
from . import unit
from .parameter import Parameter
from .rate import Rate


class MagicUnit(unit.Unit):
    __signature__ = util.make_signature([])

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for parameter in self.__signature__.parameters.values():
            if (parameter.name not in bound.arguments and
                    parameter.default is not parameter.empty):
                bound.arguments[parameter.name] = parameter.default

        if self.definition["input_rate"] == "Control":
            self.definition["input_rate"] = Rate.control
        elif self.definition["input_rate"] == "Audio":
            self.definition["input_rate"] = Rate.audio

        if self.definition["output_rate"] == "Control":
            self.definition["output_rate"] = Rate.control
        elif self.definition["output_rate"] == "Audio":
            self.definition["output_rate"] = Rate.audio

        if self.definition["kind"] == "Source":
            super(MagicUnit, self).__init__(0, bound.arguments["channels"],
                                            None,
                                            self.definition["output_rate"])
        elif self.definition["kind"] == "Sink":
            super(MagicUnit, self).__init__(bound.arguments["channels"], 0,
                                            self.definition["input_rate"],
                                            None)
        elif self.definition["kind"] == "Processor":
            super(MagicUnit, self).__init__(bound.arguments["input_channels"],
                                            bound.arguments["output_channels"],
                                            self.definition["input_rate"],
                                            self.definition["output_rate"])

        for definition in self.definition["parameters"]:
            value = bound.arguments[definition["name"]]
            parameter = Parameter(value)
            self.parameters.append(parameter)
            setattr(self, definition["name"], parameter)

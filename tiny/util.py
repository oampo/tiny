from inspect import Parameter, Signature, signature
from .parameter_proxy import ParameterProxy


def make_signature(parameters):
    return Signature(
        Parameter(
            kind=Parameter.POSITIONAL_OR_KEYWORD, **parameter
        ) for parameter in parameters
    )


def unit(function):
    function_signature = signature(function)

    def inner(*args, **kwargs):
        bound = function_signature.bind_partial(*args, **kwargs)
        for parameter in function_signature.parameters.values():
            if parameter.name in bound.arguments:
                value = bound.arguments[parameter.name]
            elif parameter.default is not parameter.empty:
                value = parameter.default
            else:
                value = None
            bound.arguments[parameter.name] = ParameterProxy(value)

        unit = function(*bound.args, **bound.kwargs)

        for name, value in bound.arguments.items():
            setattr(unit, name, value)
        return unit
    return inner

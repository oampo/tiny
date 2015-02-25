from inspect import Parameter, Signature


def make_signature(parameters):
    return Signature(
        Parameter(
            kind=Parameter.POSITIONAL_OR_KEYWORD, **parameter
        ) for parameter in parameters
    )

import os.path
import json
from inspect import Parameter, Signature

import inflection

from . import util
from . import magic_unit

with open(os.path.expanduser("~/.config/art/art_info.json")) as f:
    info = json.load(f)

for type_id, unit in enumerate(info["units"]):
    unit["type_id"] = type_id
    class_name = inflection.camelize(unit["name"])

    default_input_channels = unit["default_layout"]["input"]
    default_output_channels = unit["default_layout"]["output"]

    parameters = []
    for parameter in unit["parameters"]:
        parameters.append({
            "name": parameter["name"],
            "default": parameter["default"]
        })

    kind = unit["kind"]
    if kind == "Source":
        parameters.append({"name": "channels",
                           "default": default_output_channels})
    elif kind == "Sink":
        parameters.append({"name": "channels",
                           "default": default_input_channels})
    elif kind == "Processor":
        parameters.append({"name": "input_channels",
                           "default": default_input_channels})
        parameters.append({"name": "output_channels",
                           "default": default_input_channels})

    signature = util.make_signature(parameters)
    vars()[class_name] = type(class_name, (magic_unit.MagicUnit,),
                              dict(__signature__=signature,
                                   definition=unit))

class Adc(BusInAr):
    def __init__(self, channels=info["input_channels"]):
        super(Adc, self).__init__(channels=channels, bus_id=0.0)

class Dac(BusOutAr):
    def __init__(self, channels=info["output_channels"]):
        super(Dac, self).__init__(channels=channels, bus_id=1.0)


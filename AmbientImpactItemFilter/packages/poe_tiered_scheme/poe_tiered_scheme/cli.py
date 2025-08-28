from .DebugSchemes import DebugSchemes
from .TieredScheme import TieredScheme
from jsonargparse import ActionYesNo, ArgumentParser, auto_cli
import base64
import json

# Custom argument parser to allow boolean --flag arguments without having to do
# --flag true.
#
# @see https://jsonargparse.readthedocs.io/en/stable/#customization-of-arguments
class CustomArgumentParser(ArgumentParser):

  def add_argument(self, *args, **kwargs):

    if "type" in kwargs and kwargs["type"] == bool:

      kwargs.pop("type")

      kwargs["action"] = ActionYesNo

    return super().add_argument(*args, **kwargs)

def command(jsonString: str, debug: bool = False):

  jsonParsed = json.loads(base64.b64decode(jsonString))

  data = {}

  schemes = {}

  for name, schemeConfig in jsonParsed.items():

    schemes[name] = TieredScheme(name, schemeConfig)

    if debug == False:
      data[name] = schemes[name].dict()

  if debug == True:

    DebugSchemes(schemes).print()

  if debug == False:
    print(json.dumps(data))

def run():
  auto_cli(command, parser_class=CustomArgumentParser)

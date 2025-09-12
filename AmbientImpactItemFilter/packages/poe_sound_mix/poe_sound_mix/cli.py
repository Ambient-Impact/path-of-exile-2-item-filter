from .SoundMix import SoundMix
from jsonargparse import auto_cli
import base64
import json

def command(jsonString: str):

  jsonParsed = json.loads(base64.b64decode(jsonString))

  mix = SoundMix(jsonParsed['soundPacks'], jsonParsed['tieredSchemes'])

  print(json.dumps(mix.dict, indent=2))

def run():
  auto_cli(command)

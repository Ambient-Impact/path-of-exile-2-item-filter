from colouration import Colour
from jsonargparse import auto_cli
import base64
import json
# @todo This throws an error since we don't define a package so pls define one.
# from .tiered_colour_scheme import TieredColourScheme

class TieredColourScheme:

  def __init__(self, name: str, config: dict):

    self._name = name

    self._config = config

    rgb = config['colour']

    self._tiers = {}

    # @todo Throw error if len(rgb) is not 3? What about opacity?

    self._baseColour = Colour(
      red=rgb[0], green=rgb[1], blue=rgb[2],
      max_value=255
    )

    # S-tier.
    self._tiers['s'] = {
      'background': self._baseColour.darken(ratio=0.4).saturate(ratio=0.3),
      'border':     self._baseColour.lighten(ratio=0.1).saturate(ratio=0.5),
      'text':       self._baseColour.lighten(ratio=0.1).saturate(ratio=0.5),
    }

    # A-tier.
    self._tiers['a'] = {
      'background': self._baseColour.darken(ratio=0.55),
      'border':     self._baseColour.lighten(ratio=0.1).saturate(ratio=0.3),
      'text':       self._baseColour.lighten(ratio=0.1).saturate(ratio=0.3),
    }

    # B-tier. This is a copy of the base colour as-is with only minor adjustment
    # to the border.
    self._tiers['b'] = {
      'background': Colour('black'),
      'border':     self._baseColour.darken(ratio=0.1),
      'text':       self._baseColour,
    }

    # C tier.
    self._tiers['c'] = {
      'background': Colour('black'),
      'border':     self._baseColour.darken(ratio=0.5),
      'text':       self._baseColour.darken(ratio=0.1),
    }

    # D tier.
    self._tiers['d'] = {
      'background': Colour('black'),
      'border':     Colour('black'),
      'text':       self._baseColour.darken(ratio=0.2).pale(ratio=0.1),
    }

    # E tier.
    self._tiers['e'] = {
      'background': Colour('black'),
      'border':     Colour('black'),
      'text':       self._baseColour.darken(ratio=0.35).pale(ratio=0.1),
    }

  def preview(self, text: str, colours: dict):

    # This prevents a dumb error that occurs when passing a Colour object as the
    # 'secondary' parameter.
    #
    # @todo Open an issue: https://github.com/idin/colouration
    backgroundHex = colours['background'].get_hexadecimal();

    textLength = len(text)

    colours['border'].print(
      '⎡⎺' + '⎺' * textLength + '⎺⎤',
      main_colour='text', secondary=backgroundHex,
    )
    colours['border'].print(
      '| ', main_colour='text', secondary=backgroundHex, end='',
    )
    colours['text'].print(
      text, main_colour='text', secondary=backgroundHex, end='',
    )
    colours['border'].print(' |', main_colour='text', secondary=backgroundHex)
    colours['border'].print(
      '⎣⎽' + '⎽' * textLength + '⎽⎦',
      main_colour='text', secondary=backgroundHex,
    )

  def debug(self):

    print(self._name)

    self.preview('S tier', self._tiers['s'])
    self.preview('A tier', self._tiers['a'])
    self.preview('B tier', self._tiers['b'])
    self.preview('C tier', self._tiers['c'])
    self.preview('D tier', self._tiers['d'])
    self.preview('E tier', self._tiers['e'])

    print(self.dict())

  @staticmethod
  def formatColour(colour):

    minimum = 0
    maximum = 255

    return [
      min(maximum, max(minimum, round(colour.red    * maximum))),
      min(maximum, max(minimum, round(colour.green  * maximum))),
      min(maximum, max(minimum, round(colour.blue   * maximum))),
    ]

  # @see https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields/75390673#75390673
  #  Can we use a data class and JSON serializer for this instead?
  def dict(self):

    data = {
      'tiers': {}
    }

    for tierName, colours in self._tiers.items():

      data['tiers'][tierName] = {
        'background': self.formatColour(colours['background']),
        'border':     self.formatColour(colours['border']),
        'text':       self.formatColour(colours['text']),
      }

    return data

def command(jsonString: str, debug: bool = False):

  jsonParsed = json.loads(base64.b64decode(jsonString))

  data = {}

  for name, schemeConfig in jsonParsed.items():

    scheme = TieredColourScheme(name, schemeConfig)

    if debug == True:
      scheme.debug()

    data[name] = scheme.dict()

  if debug == False:
    print(json.dumps(data))

if __name__ == '__main__':
  auto_cli(command)

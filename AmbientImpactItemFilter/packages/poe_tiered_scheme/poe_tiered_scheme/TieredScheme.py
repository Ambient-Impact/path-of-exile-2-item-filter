from colouration import Colour
from .MixedColour import MixedColour

class TieredScheme:

  def __init__(self, name: str, config: dict):

    self._name = name

    self._config = config

    rgb = config['colour']

    self._tiers = {}

    # @todo Throw error if len(rgb) is not 3? What about opacity?

    self._baseColour = Colour(
      red=rgb[0], green=rgb[1], blue=rgb[2],
      max_value=255,
    )

    # S-tier.
    self._tiers['s'] = {
      'background': MixedColour(self._baseColour).mixWithBlack(0.5),
      'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
      'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
    }

    # A-tier.
    self._tiers['a'] = {
      'background': MixedColour(self._baseColour).mixWithBlack(0.75),
      'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
      'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
    }

    # B-tier. This is a copy of the base colour as-is with only minor adjustment
    # to the border.
    self._tiers['b'] = {
      'background': MixedColour(self._baseColour).mixWithBlack(0.85),
      'border':     MixedColour(self._baseColour).mixWithBlack(0.1),
      'text':       self._baseColour,
    }

    # C tier.
    self._tiers['c'] = {
      'background': Colour('black'),
      'border':     MixedColour(self._baseColour).mixWithBlack(0.5),
      'text':       MixedColour(self._baseColour).mixWithBlack(0.2),
    }

    # D tier.
    self._tiers['d'] = {
      'background': Colour('black'),
      'border':     MixedColour(self._baseColour).mixWithBlack(0.8),
      'text':       MixedColour(self._baseColour).mixWithBlack(0.3),
    }

    # E tier.
    self._tiers['e'] = {
      'background': Colour('black'),
      'border':     Colour('black'),
      'text':       MixedColour(self._baseColour).mixWithBlack(0.4),
    }

  def preview(self, text: str, colours: dict) -> None:

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

  def debug(self) -> None:

    print(self._name)

    self.preview('S tier', self._tiers['s'])
    self.preview('A tier', self._tiers['a'])
    self.preview('B tier', self._tiers['b'])
    self.preview('C tier', self._tiers['c'])
    self.preview('D tier', self._tiers['d'])
    self.preview('E tier', self._tiers['e'])

    print(self.dict())

  @staticmethod
  def formatColour(colour) -> list:

    minimum = 0
    maximum = 255

    return [
      min(maximum, max(minimum, round(colour.red    * maximum))),
      min(maximum, max(minimum, round(colour.green  * maximum))),
      min(maximum, max(minimum, round(colour.blue   * maximum))),
    ]

  # @see https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields/75390673#75390673
  #  Can we use a data class and JSON serializer for this instead?
  def dict(self) -> dict:

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

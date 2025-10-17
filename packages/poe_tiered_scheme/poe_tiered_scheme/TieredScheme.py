from poe_colour.MixedColour import MixedColour
from poe_colour.PoeColour import PoeColour

class TieredScheme:

  def __init__(self, name: str, config: dict):

    self.name = name

    self._config = config

    rgb = config['colour']

    self._tiers = {}

    self._baseColour = PoeColour(config['colour'])

    black = PoeColour((0, 0, 0))

    # Default this to False if not set to simplify handling it later.
    if 'rarityColour' not in config:

      config['rarityColour'] = False

    # S-tier.
    if config['rarityColour'] == False:

      # Invert S-tier if not using rarity colours.
      self._tiers['s'] = {
        'background': MixedColour(self._baseColour).mixWithWhite(0.1),
        'border':     black,
        'text':       black,
      }

    else:

      self._tiers['s'] = {
        'background': MixedColour(self._baseColour).mixWithBlack(0.4),
        'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
        'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
      }

    # A-tier.
    if config['rarityColour'] == False:

      # Equivalent of S-tier with rarity colours.
      self._tiers['a'] = {
        'background': MixedColour(self._baseColour).mixWithBlack(0.4),
        'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
        'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
      }

    else:

      self._tiers['a'] = {
        'background': MixedColour(self._baseColour).mixWithBlack(0.75),
        'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
        'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
      }

    # B-tier.
    if config['rarityColour'] == False:

      # Equivalent of A-tier with rarity colours.
      self._tiers['b'] = {
        'background': MixedColour(self._baseColour).mixWithBlack(0.75),
        'border':     MixedColour(self._baseColour).mixWithWhite(0.1),
        'text':       MixedColour(self._baseColour).mixWithWhite(0.1),
      }

    else:

      self._tiers['b'] = {
        'background': MixedColour(self._baseColour).mixWithBlack(0.85),
        'border':     MixedColour(self._baseColour).mixWithBlack(0.1),
        'text':       self._baseColour,
      }

    # C tier.
    self._tiers['c'] = {
      'background': black,
      'border':     MixedColour(self._baseColour).mixWithBlack(0.5),
      'text':       MixedColour(self._baseColour).mixWithBlack(0.2),
    }

    # D tier.
    self._tiers['d'] = {
      'background': black,
      'border':     MixedColour(self._baseColour).mixWithBlack(0.8),
      'text':       MixedColour(self._baseColour).mixWithBlack(0.3),
    }

    # E tier.
    self._tiers['e'] = {
      'background': black,
      'border':     black,
      'text':       MixedColour(self._baseColour).mixWithBlack(0.4),
    }

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    self._name = name

  @property
  def tiers(self) -> dict:
    return self._tiers

  @tiers.setter
  def tiers(self, tiers: dict) -> None:
    self._tiers = tiers

  # @see https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields/75390673#75390673
  #  Can we use a data class and JSON serializer for this instead?
  def dict(self) -> dict:

    data = {
      'tiers': {}
    }

    for tierName, colours in self._tiers.items():

      data['tiers'][tierName] = {
        'background': colours['background'].rgba,
        'border':     colours['border'].rgba,
        'text':       colours['text'].rgba,
      }

    return data

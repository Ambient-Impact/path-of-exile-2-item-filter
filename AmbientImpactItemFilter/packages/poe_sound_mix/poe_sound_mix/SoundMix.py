from .SoundPack import SoundPack

class SoundMix:

  def __init__(self, packs: dict, tieredSchemes: dict):

    self._packs = {}

    self._tieredSchemes = tieredSchemes

    for name, packData in packs.items():

      self.addPack(name, packData)

  def addPack(self, name: str, packData: dict) -> None:

    self._packs[name] = SoundPack(name, packData)

  def createMix(self) -> dict:

    mix = {}

    for schemeName, scheme in self._tieredSchemes.items():

      if ('sounds' not in scheme):

        continue

      mix[schemeName] = {}

      # @todo Add arrays, etc.
      if (
        isinstance(scheme['sounds'], str) and
        scheme['sounds'] in self._packs
      ):

        self._packs[scheme['sounds']].applyToScheme(
          schemeName, mix[schemeName],
        )

    return mix

  @property
  def dict(self) -> dict:

    return self.createMix()

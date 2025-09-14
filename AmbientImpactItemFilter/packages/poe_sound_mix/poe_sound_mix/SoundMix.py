from .SoundConfig import SoundConfig
from .SoundPack import SoundPack
from dataclasses import dataclass

@dataclass
class SoundMix:
  """Represents a mix of sound packs based on tiered schemes configuration."""

  _packs: dict

  _tieredSchemes: dict

  def __post_init__(self) -> None:

    packs = self._packs.copy()

    self._packs = {}

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

      soundConfig = SoundConfig(schemeName, scheme)

      for packName in soundConfig.packNames:

        if (packName not in self._packs):

          raise Exception(
            f'Sound pack "{packName}" requested by the "{schemeName}" scheme doesn\'t exist.',
          )

        self._packs[scheme['sounds']].applyToScheme(
          schemeName, mix[schemeName],
        )

    return mix

  @property
  def packs(self) -> dict[str, SoundPack]:

    return self._packs

  @property
  def dict(self) -> dict:

    return self.createMix()

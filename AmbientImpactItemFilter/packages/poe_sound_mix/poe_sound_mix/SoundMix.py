from .SoundPack import SoundPack

class SoundMix:

  def __init__(self, packs: dict):

    self._packs = {}

    for name, packData in packs.items():

      self.addPack(name, packData)

  def addPack(self, name: str, packData: dict) -> None:

    self._packs[name] = SoundPack(name, packData)

  @property
  def dict(self) -> dict:

    packs = {}

    for name, pack in self._packs.items():

      packs[name] = pack.dict

    return packs

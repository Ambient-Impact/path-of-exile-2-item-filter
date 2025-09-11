class SoundPack:

  def __init__(self, name: str, packData: dict):

    self._name = name

    self._packData = packData

  @property
  def dict(self) -> dict:

    return self._packData

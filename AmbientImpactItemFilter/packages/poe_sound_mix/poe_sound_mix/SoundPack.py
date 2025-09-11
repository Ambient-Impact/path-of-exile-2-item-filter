from pathlib import PurePath

class SoundPack:

  def __init__(self, name: str, packData: dict):

    self._name = name

    for soundName, soundFile in packData['sounds'].items():

      # Build the path for each sound file.
      packData['sounds'][soundName] = str(PurePath(packData['path'], soundFile))

    self._packData = packData

  @property
  def dict(self) -> dict:

    return self._packData

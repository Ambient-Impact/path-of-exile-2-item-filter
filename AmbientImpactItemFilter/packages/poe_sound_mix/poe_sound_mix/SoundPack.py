from pathlib import PurePath

class SoundPack:

  def __init__(self, name: str, packData: dict):

    self._name = name

    self._packData = packData

    self._buildSoundPaths()

    self._buildTieredSchemes()

  def _buildSoundPaths(self) -> None:

    packData = self._packData

    for soundName, soundFile in packData['sounds'].items():

      # Build the path for each sound file.
      packData['sounds'][soundName] = str(PurePath(packData['path'], soundFile))

  def _buildTieredSchemes(self) -> None:

    packData = self._packData

    if ('tieredSchemes' not in packData):

      return

    sounds = packData['sounds']

    schemes = packData['tieredSchemes']

    for schemeName, scheme in schemes.items():

      for tierName, soundName in scheme.items():

        if (soundName not in sounds):

          raise Exception(
            f'Sound "{soundName}" doesn\'t exist in the "{self._name}" sound pack.',
          )

        scheme[tierName] = sounds[soundName]

  def applyToScheme(self, schemeName: str, scheme: dict) -> dict:

    packData = self._packData

    if (
      'tieredSchemes' not in packData or
      schemeName not in packData['tieredSchemes']
    ):

      return

    if ('tiers' not in scheme):

      scheme['tiers'] = {}

    for tierName, sound in packData['tieredSchemes'][schemeName].items():

      if (tierName not in scheme['tiers']):

        scheme['tiers'][tierName] = {}

      scheme['tiers'][tierName] = scheme['tiers'][tierName] | {'sound': sound}

  @property
  def dict(self) -> dict:

    return self._packData

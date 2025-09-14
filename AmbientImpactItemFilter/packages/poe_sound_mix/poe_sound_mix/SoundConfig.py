from .SoundPack import SoundPack
from dataclasses import dataclass, field

@dataclass
class SoundConfig:
  """Represents a tiered scheme sound configuration."""

  _schemeName: str

  _scheme: dict

  # @see https://stackoverflow.com/questions/51079503/dataclasses-and-property-decorator/61191878#61191878
  _packNames: list[str] = field(init=False, repr=False)

  def __post_init__(self) -> None:

    self._parseConfig()

  def _parseConfig(self) -> None:

    self._packNames = []

    if (isinstance(self._scheme['sounds'], str)):

      self._packNames = [self._scheme['sounds']]

    elif (isinstance(self._scheme['sounds'], list)):

      self._packNames = self._scheme['sounds']

    elif (isinstance(self._scheme['sounds'], dict)):

      if ('pack' not in self._scheme['sounds']):

        raise Exception(
          f'The sound configuration for "{self._schemeName}" must have a "pack" key.',
        )

      if ('from' not in self._scheme['sounds']):

        self._packNames.append(self._scheme['sounds']['pack'])

        return

      # @todo Now we need to return a way to use a different tier name instead
      #  of the specified one so that a scheme can specify using or inheriting
      #  from another scheme so packs don't need to set for every scheme.

  @property
  def packNames(self) -> list[str]:

    return self._packNames

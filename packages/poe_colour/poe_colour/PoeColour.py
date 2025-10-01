from colouration import Colour
from typing import Tuple

COLOUR_MIN = 0
COLOUR_MAX = 255

class PoeColour:

  def __init__(self, rgba: Tuple[int, int, int] | Tuple[int, int, int, int]):

    self.red    = int(rgba[0])
    self.green  = int(rgba[1])
    self.blue   = int(rgba[2])

    if (len(rgba) == 4):

      self.opacity = int(rgba[3])

    else:

      self.opacity = COLOUR_MAX

    self._colour = Colour(
      red=self._red, green=self._green, blue=self._blue,
      max_value=COLOUR_MAX,
    )

  def _validatePropertyValue(self, name: str, value: int) -> int:

    if (value >= COLOUR_MIN) & (value <= COLOUR_MAX):
      return value

    raise Exception(f'Property "{name}" must be between {COLOUR_MIN} and {COLOUR_MAX} inclusive; got "{value}".')

  @property
  def red(self) -> int:

    return self._red

  @red.setter
  def red(self, value: int) -> None:

    self._red = self._validatePropertyValue('red', value)

  @property
  def green(self) -> int:

    return self._green

  @green.setter
  def green(self, value: int) -> None:

    self._green = self._validatePropertyValue('green', value)

  @property
  def blue(self) -> int:

    return self._blue

  @blue.setter
  def blue(self, value: int) -> None:

    self._blue = self._validatePropertyValue('blue', value)

  @property
  def opacity(self) -> int:

    return self._opacity

  @opacity.setter
  def opacity(self, value: int) -> None:

    self._opacity = self._validatePropertyValue('opacity', value)

  @property
  def rgb(self) -> Tuple[int, int, int]:

    return (self._red, self._green, self._blue)

  @property
  def rgba(self) -> Tuple[int, int, int, int]:

    return (self._red, self._green, self._blue, self._opacity)

  @property
  def hexadecimal(self, opacity: bool = False) -> str:

    if (opacity == False):

      return self._colour.get_hexadecimal()

    return self._colour.get_hexadecimal(opacity=self._opacity)

  @property
  def colour(self) -> Colour:

    return self._colour

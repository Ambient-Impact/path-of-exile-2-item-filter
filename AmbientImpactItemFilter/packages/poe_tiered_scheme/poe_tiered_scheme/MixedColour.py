from colouration import Colour
from typing import Tuple
import mixbox

class MixedColour:

  def __init__(self, colour: Colour):

    self._colour = colour

    self._tuple = self.formatTuple(colour)

  def mixWith(self, colour: tuple, weight: float) -> Colour:

    mixed = mixbox.lerp(self._tuple, colour, weight)

    return Colour(
      red=mixed[0], green=mixed[1], blue=mixed[2],
      max_value=255,
    )

  def mixWithBlack(self, weight: float) -> Colour:

    return self.mixWith((0, 0, 0), weight)

  def mixWithWhite(self, weight: float) -> Colour:

    return self.mixWith((255, 255, 255), weight)

  @staticmethod
  def formatTuple(colour) -> Tuple[int, int, int]:

    minimum = 0
    maximum = 255

    return (
      min(maximum, max(minimum, round(colour.red    * maximum))),
      min(maximum, max(minimum, round(colour.green  * maximum))),
      min(maximum, max(minimum, round(colour.blue   * maximum))),
    )

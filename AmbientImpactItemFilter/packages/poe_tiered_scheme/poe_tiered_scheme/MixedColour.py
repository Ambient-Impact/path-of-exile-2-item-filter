from typing import Tuple
import mixbox
from poe_colour.PoeColour import PoeColour

class MixedColour:

  def __init__(self, colour: PoeColour):

    self._colour = colour

  def mixWith(self, colour: tuple, weight: float) -> PoeColour:

    mixed = mixbox.lerp(self._colour.rgb, colour, weight)

    return PoeColour(mixed)

  def mixWithBlack(self, weight: float) -> PoeColour:

    return self.mixWith((0, 0, 0), weight)

  def mixWithWhite(self, weight: float) -> PoeColour:

    return self.mixWith((255, 255, 255), weight)

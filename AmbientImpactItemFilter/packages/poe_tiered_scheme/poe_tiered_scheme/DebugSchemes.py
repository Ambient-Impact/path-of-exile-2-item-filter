from .TieredScheme import TieredScheme
from colouration import Colour
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Dict

class DebugSchemes:

  def __init__(self, schemes: Dict[str, TieredScheme]):

    self._schemes = schemes

  @staticmethod
  def _cell(title: str, tier: Dict[str, Colour]) -> Panel:

    return Panel(
      title,
      style=f'{tier['text'].get_hexadecimal()} on {tier['background'].get_hexadecimal()}',
      border_style=f'{tier['border'].get_hexadecimal()}',
    )

  def print(self) -> None:

    console = Console()

    table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))

    table.add_column('Name')
    table.add_column('S tier')
    table.add_column('A tier')
    table.add_column('B tier')
    table.add_column('C tier')
    table.add_column('D tier')
    table.add_column('E tier')

    for name, scheme in self._schemes.items():

      table.add_row(
        name,
        self._cell('S tier', scheme.tiers['s']),
        self._cell('A tier', scheme.tiers['a']),
        self._cell('B tier', scheme.tiers['b']),
        self._cell('C tier', scheme.tiers['c']),
        self._cell('D tier', scheme.tiers['d']),
        self._cell('E tier', scheme.tiers['e']),
      )

    console.print(table)

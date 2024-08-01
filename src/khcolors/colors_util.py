# colors_util.py

from matplotlib.colors import CSS4_COLORS
from matplotlib import colors as mcolors
from rich.color import ANSI_COLOR_NAMES
from rich.console import Console
from rich.text import Text
import pyperclip
from platform import system

ftitle = __file__.split("/", maxsplit=-1)[-1].split(".", maxsplit=-1)[0]

CN = Console()
cprint = CN.print

COLOR_BASE = {'css': CSS4_COLORS, 'rich': ANSI_COLOR_NAMES}
# markers for colour samples:
MARKER0 = "\u00a0"
# MARKER1 = "x"  # \u2501
# MARKER1 = "\u25cf"  # ●
# MARKER1 = "◉"
if system().lower() != "windows":  # platform.
    MARKER1 = "⏺"  # \u23fa
else:
    MARKER1 = "o"


def byte_rgb(color):
    """ Converts color to r, g, b in range [0, 1], to range [0, 255] """

    r, g, b = [item*255 for item in mcolors.to_rgb(color)]

    return f"rgb({r:.0f},{g:.0f},{b:.0f})"


def get_color_name(search_for: str, palette: str = "rich") -> None:
    """ Getting the colour name from rich or CSS4 palettes

        Args:
            search_for (str): name (or part of the name) of the colour
                              to look for.
            palette (str): the palette to search the color, 'rich' or 'css'

        Returns:
            None: the application prints a list of colours found and allows
            copying a chosen name to clipboard.
    """

    colors_base = COLOR_BASE[palette]
    found = []
    # looking for match(es):
    for color in colors_base:
        found.append(color) if search_for in color else None
    if not found:
        if search_for == "name":
            msg = Text.assemble(("Looking for color name ", ""),
                                (f"{search_for}", "bold italic"),
                                (" -- ", ""),
                                ("seriously?", "bold italic red"))
            cprint(msg)
            return
        cprint(Text.assemble(("No color found for '", ""),
               (f"{search_for}", "bold"), ("', exiting.", "")))
        return
    cprint(" Choose colour (number):", style="bold")
    marg = len(str(len(found)))
    for i, color in enumerate(found):
        print_color(i, color, color_base=palette, marg=marg)

    nr_to_copy = None
    while nr_to_copy is None:
        try:
            to_copy = input(f"Color name to copy? (0-{i}; <Enter> to exit): ")
            if to_copy == "":
                return
            nr_to_copy = int(to_copy)
            if 0 <= nr_to_copy <= i:
                chosen_color = found[nr_to_copy]
                if palette == "css":
                    color_code = byte_rgb(chosen_color)
                else:
                    color_code = chosen_color
                pyperclip.copy(chosen_color)
                msg = Text("Color ")
                msg.append(chosen_color, style=f"bold italic {color_code}")
                msg.append(" copied to clipboard.")
                cprint(msg)
                return
            cprint(f"Number should have been 0 ≤ i ≤ {i}. Not copying.")
            nr_to_copy = None
        except ValueError:
            cprint("Wrong number, leave empty to exit.")


def print_color(i, name, color_base="rich", marg=3):
    """ Printing a color tile """

    clr = name if color_base == "rich" else byte_rgb(name)
    tile_len = 7
    color_tile = Text(f"{i:>{marg}}. ")
    color_tile.append(MARKER0*tile_len, style=f"white on {clr}")
    if system().lower != "windows":  # platform.
        color_tile.append(MARKER1*tile_len, style=f"bold black on {clr}")
        color_tile.append(MARKER1*tile_len, style=f"bold white on {clr}")
    color_tile.append(MARKER0*tile_len, style=f"white on {clr}")
    color_tile.append(f" {name}", style="white on black")
    cprint(color_tile)

# src/khcolors/__main__.py

import argparse
from rich.console import Console

from .colors_util import get_color_name

projtitle = "khcolors"

CN = Console()
cprint = CN.print


def main():
    """ Entry point """

    desc = ("searching for a css colour or a colour in the rich library. "
            "result: list of all the colours with `name` in them. "
            "(`name` may contain only a part of the colour name.)")
    epilog = ("example: python colours.py red;\n"
              "python colours.py sea")
    parser = argparse.ArgumentParser(prog=f"python {projtitle}",
                                     description=desc, epilog=epilog)
    parser.add_argument("name", type=str, help="name of the colour "
                        "to look for (required)")
    # kind_of_colours, rich, css kind or all:
    # kind_of_colours_group = ["css", "rich"]
    kind_of_colours = parser.add_mutually_exclusive_group(required=False)
    kind_of_colours.add_argument("-i", "--rich", action="store_true",
                                 help="rich named colours (default)")
    kind_of_colours.add_argument("-c", "--css", action="store_true",
                                 default=False, help="css4 colours")
    parser.add_argument("-a", "--all", action="store_true",
                        default=False,
                        help="showing all the colours in the rich "
                        "library")

    args = parser.parse_args()
    palette = "rich" if args.rich else ("css" if args.css else "rich")

    get_color_name(args.name, palette)


if __name__ == "__main__":
    main()

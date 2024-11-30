# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: parser.py
# License: GPL-3

import argparse


class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        """Remove metavar from 'options:' list."""
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []
            # Format options like:
            #    -s, --long <help>
            parts.extend(action.option_strings)

            return ", ".join(parts)

    def _get_default_metavar_for_optional(self, action):
        """Use argument 'type' as the default metavar value when possible."""
        try:
            return action.type.__name__
        except AttributeError:
            return action.dest


def argparser():
    METHODS = ("pseudo", "sobol", "halton", "latin")

    parser = argparse.ArgumentParser(
        add_help=False,
        description=(
            "Microstructure Modeling and Simulation."
            " Generate microstructures using site-saturation condition,"
            " and simulate grain growth using Monte Carlo Potts Model."
        ),
        formatter_class=CustomFormatter,
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )
    parser.add_argument(
        "-w",
        "--width",
        default=500,
        type=int,
        help="Set the application window width. (default: 500)",
    )
    parser.add_argument(
        "-c",
        "--cell-size",
        dest="grid_cell_size",
        default=5,
        type=int,
        help="Define the grid cell size. Lower values result in sharper boundaries. (default: 5, recommended range: 1-10)",
    )
    parser.add_argument(
        "-o",
        "--orientations",
        default=100,
        type=int,
        help="Specify the initial number of grains. Higher values produce smaller grains. (default: 100)",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="halton",
        choices=METHODS,
        dest="seed_method",
        type=str,
        help=f"Choose the seed generation algorithm. Allowed values are: {', '.join(METHODS)}. (default: halton)",
    )
    parser.add_argument(
        "-T",
        "--temperature",
        default=0,
        type=float,
        help="Set the simulation temperature. Higher values increase the likelihood of unfavorable grain boundary migration. (default: 0, recommended range: 0-2)",
    )
    parser.add_argument(
        "-b",
        "--boltz",
        dest="boltz_const",
        default=1,
        type=float,
        help="Specify the Boltzmann constant. (default: 1)",
    )
    parser.add_argument(
        "-g",
        "--grain",
        dest="grain_boundary_energy",
        default=1,
        type=float,
        help="Set the grain boundary energy. (default: 1)",
    )
    parser.add_argument(
        "--simulate",
        default=False,
        help="Enable grain growth simulation. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--color",
        default=False,
        help="Display grains in color instead of grayscale. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--snapshot",
        default=0,
        type=int,
        help=(
            "Save snapshots of the microstructure at specified intervals (in seconds). Without simulation, only one snapshot is saved. (default: never)"
        ),
    )
    parser.add_argument(
        "--save",
        default=False,
        help="Save microstructure data to a file. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--load",
        type=str,
        help=(
            "Load microstructure data from a file. This option can override or be combined with other options like --temperature, --grain, --boltz, --simulate, --color, and --snapshot."
        ),
    )
    parser.add_argument(
        "-hb",
        "--highlight-boundaries",
        type=str,
        help=(
            "Process snapshots of a microstructure from a specified folder to extract and display only grain boundaries. The processed snapshots are saved with highlighted grain boundaries, removing the original colored grain representation."
            "Note: This requires imagemagick (https://imagemagick.org) to be installed."
        ),
    )

    return parser.parse_args()

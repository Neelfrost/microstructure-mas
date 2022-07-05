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


def parser():
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
        help="Application window size. (default: 500)",
    )
    parser.add_argument(
        "-c",
        "--cell-size",
        dest="cell_size",
        default=5,
        type=int,
        help="Grid cell size, lower = sharper boundaries. (default: 5, recommended: 1-10)",
    )
    parser.add_argument(
        "-o",
        "--orientations",
        default=100,
        type=int,
        help="Inital grain size, higher = smaller grains. (default: 100)",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="sobol",
        choices=METHODS,
        type=str,
        help=f"Seed generation algorithm. Allowed values are: {', '.join(METHODS)}. (default: sobol)",
    )
    parser.add_argument(
        "-T",
        "--temperature",
        default=0,
        type=float,
        help="Simulation temperature. (default: 0, recommended: 0-2)",
    )
    parser.add_argument(
        "-b",
        "--boltz",
        default=1,
        type=float,
        help="Boltzmann constant. (default: 1)",
    )
    parser.add_argument(
        "-g",
        "--grain",
        default=1,
        type=float,
        help="Grain boundary energy. (default: 1)",
    )
    parser.add_argument(
        "--simulate",
        default=False,
        help="Simulate grain growth. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--color",
        default=False,
        help="Instead of using grayscale, display colored grains. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--snapshot",
        default=0,
        type=int,
        help=(
            "Every specified number of seconds, save images of the microstructure."
            " Only one image is saved without simulation. (default: never)"
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
        help="Load microstructure data from a file.",
    )

    return parser.parse_args()

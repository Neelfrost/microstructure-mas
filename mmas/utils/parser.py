# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: parser.py
# License: GPL-3

import argparse


def parser():
    # Init parser
    parser = argparse.ArgumentParser(
        description=(
            "Microstructure Modeling and Simulation."
            " Generate microstructures using site-saturation condition,"
            " and simulate grain growth using Monte Carlo Potts Model."
        ),
    )
    # Add args
    parser.add_argument(
        "-w",
        "--width",
        default=500,
        type=int,
        help="Window size. (default: 500)",
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
        choices=("pseudo", "sobol", "halton", "latin"),
        type=str,
        help="Seed generation algorithm. (default: sobol)",
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
        help="Simulate grain growth? (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--color",
        default=False,
        help="Show colored grains instead of grayscale. (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "--snapshot",
        default=0,
        type=int,
        help=(
            "Save snapshots of microstructure every _ seconds."
            " Will save only one snapshot without simulation. (default: never)"
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
        type=TextIOBase,
        help="Load microstructure data from a file.",
    )

    # Return args namespace
    return parser.parse_args()



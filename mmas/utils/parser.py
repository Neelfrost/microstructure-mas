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
        help="Cell size. Lower = more anti-aliased. (default: 5, recommended: 1-10)",
    )
    parser.add_argument(
        "-o",
        "--orientations",
        default=100,
        type=int,
        help="Inital grain size. Higher = Smaller grains. (default: 100)",
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
        "--simulate",
        default=False,
        help="Simulate grain growth?",
        action="store_true",
    )
    parser.add_argument(
        "--color",
        default=False,
        help="Show colored grains instead of gray scale",
        action="store_true",
    )
    parser.add_argument(
        "--snapshot",
        default=0,
        type=int,
        help="Save snapshots of microstructure every _ seconds. Will save only one snapshot without simulation. (default: never)",
    )

    # Return args namespace
    return parser.parse_args()



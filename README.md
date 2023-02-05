<p align="center">
    <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/microstructure-mas/icon.gif" alt="slideshare-dl logo" width="192">
</p>

<h1 align="center">Microstructure Modeling and Simulation</h1>

<p align="center">
  This repository contains a program to generate microstructures using a site-saturation condition and simulate grain growth using the Monte Carlo Potts Model. The generated microstructures can be used as initial conditions for the grain growth simulation, which can be used to study the evolution of grain boundaries over time.
</p>

https://user-images.githubusercontent.com/64243795/172417152-be09b5d2-f71e-4dc0-8d4f-c78993d95f70.mp4

## Installation

1. Download repository:

   Without Git:

   ```
   curl.exe -LJO https://github.com/Neelfrost/microstructure-mas/archive/refs/heads/main.zip; Expand-Archive -Force .\microstructure-mas-main.zip .; cd .\microstructure-mas-main
   ```

   With Git:

   ```
   git clone https://github.com/Neelfrost/microstructure-mas; cd .\microstructure-mas
   ```

2. Install using pip:

   ```
   pip install .
   ```

## Usage

```
mmas.exe --help
```

```
usage: mmas [-h] [-w int] [-c int] [-o int] [-m {pseudo,sobol,halton,latin}] [-T float] [-b float] [-g float]
            [--simulate] [--color] [--snapshot int] [--save] [--load str]

Microstructure Modeling and Simulation. Generate microstructures using site-saturation condition, and simulate grain
growth using Monte Carlo Potts Model.

options:
  -h, --help          Show this message and exit.
  -w, --width         Application window size. (default: 500)
  -c, --cell-size     Grid cell size, lower = sharper boundaries. (default: 5, recommended: 1-10)
  -o, --orientations  Inital grain size, higher = smaller grains. (default: 100)
  -m, --method        Seed generation algorithm. Allowed values are: pseudo, sobol, halton, latin. (default: sobol)
  -T, --temperature   Simulation temperature. (default: 0, recommended: 0-2)
  -b, --boltz         Boltzmann constant. (default: 1)
  -g, --grain         Grain boundary energy. (default: 1)
  --simulate          Simulate grain growth. (default: false)
  --color             Instead of using grayscale, display colored grains. (default: false)
  --snapshot          Every specified number of seconds, save images of the microstructure. Only one image is saved
                      without simulation. (default: never)
  --save              Save microstructure data to a file. (default: false)
  --load              Load microstructure data from a file.

```

The program parameters, such as the number of grains, and the temperature of the Potts Model, can be adjusted as per above.

## Resulting Microstructures

|                                                                                   Pseudo                                                                                   |                                                                                  Sobol                                                                                   |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/microstructure-mas/micro_w600_c2_mpseudo_o500_mcs0_t0.png" alt="pseudo" width="400" height="400"> | <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/microstructure-mas/micro_w600_c2_msobol_o500_mcs0_t0.png" alt="sobol" width="400" height="400"> |

|                                                                                   Halton                                                                                   |                                                                                  Latin Hypercube                                                                                   |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/microstructure-mas/micro_w600_c2_mhalton_o500_mcs0_t0.png" alt="halton" width="400" height="400"> | <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/microstructure-mas/micro_w600_c2_mlatin_o500_mcs0_t0.png" alt="latin-hypercube" width="400" height="400"> |

## Limitations

The program is intended to provide a qualitative understanding of the grain growth process, and is not intended to be used for quantitative predictions or engineering applications.

## References

1. Paulo Blikstein, André Paulo Tschiptschin, Monte Carlo Simulation of Grain Growth.
2. S. Sista And T. Debroy, Three-Dimensional Monte Carlo Simulation of Grain Growth in Zone-Refined Iron.
3. N. Maazi, Conversion of Monte Carlo Steps to Real Time for Grain Growth Simulation.

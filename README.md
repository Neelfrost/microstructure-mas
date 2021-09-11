## Usage

Clone repo:

```powershell
git clone https://github.com/Neelfrost/grain-py.git grain_py; cd .\grain_py\
```

Install dependencies:

```powershell
pip install -I -r requirements.txt
```

Run script:

```powershell
py .\main.py -h
```

```powershell
usage: main.py [-h] [-w WIDTH] [-c CELL_SIZE] [-o ORIENTATIONS] [-m {pseudo,sobol,halton,latin}]
               [--simulate | --no-simulate] [--save | --no-save] [--load READ]

Generate microstructures and simulate their grain growth.

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTH              Window size. (default: 500)
  -c CELL_SIZE          Cell size. Lower = more anti-aliased. (default: 5, recommended: 1-10)
  -o ORIENTATIONS       Inital grain size. Higher = Smaller grains. (default: 100)
  -m {pseudo,sobol,halton,latin}
                        Seed generation algorithm. (default: sobol)
  --simulate, --no-simulate
                        Simulate grain growth? (default: False)
  --save, --no-save     Output generated microstructure to a file? (default: False)
  --load READ           Load microstructure data from a .json file
```

## Resulting Grain Structures

|                                           Pseudo                                           |                                          Sobol                                           |
| :----------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| ![pseudo](https://raw.githubusercontent.com/Neelfrost/github-assets/main/grain/pseudo.png) | ![sobol](https://raw.githubusercontent.com/Neelfrost/github-assets/main/grain/sobol.png) |

|                                           Halton                                           |                                          Latin Hypercube                                           |
| :----------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
| ![halton](https://raw.githubusercontent.com/Neelfrost/github-assets/main/grain/halton.png) | ![latin-hypercube](https://raw.githubusercontent.com/Neelfrost/github-assets/main/grain/latin.png) |

## References

1. Paulo Blikstein, André Paulo Tschiptschin, Monte Carlo Simulation of Grain Growth.
2. S. Sista And T. Debroy, Three-Dimensional Monte Carlo Simulation of Grain Growth in Zone-Refined Iron.
3. N. Maazi, Conversion of Monte Carlo Steps to Real Time for Grain Growth Simulation.

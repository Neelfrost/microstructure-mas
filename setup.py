from setuptools import setup


def read_contents(fname):
    with open(fname, encoding="utf-8") as f:
        return f.read()


setup(
    name="microstructure-mas",
    version="0.2.5",
    description=(
        "Microstructure Modeling and Simulation."
        " Generate microstructures using site-saturation condition,"
        " and simulate grain growth using Monte Carlo Potts Model."
    ),
    author="Neel Basak",
    author_email="neelfrost@gmail.com",
    license=read_contents("LICENSE"),
    packages=["mmas", "mmas/core", "mmas/utils"],
    package_data={"mmas": ["assets/icon.png"]},
    install_requires=read_contents("requirements.txt").splitlines(),
    entry_points={"console_scripts": ["mmas = mmas.__main__:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: GPL-3",
        "Operating System :: OS Independent",
    ],
    data_files=[("", ["LICENSE"])],
)

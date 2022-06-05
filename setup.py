from setuptools import setup


def read_contents(fname):
    with open(fname, encoding="utf-8") as f:
        return f.read()


setup(
    name="Microstructural Modeling",
    version="0.1",
    description=(
        "Generate microstructures using site-saturation condition,"
        " and simulate grain growth using Monte Carlo Potts Model."
    ),
    author="Neel Basak",
    author_email="neelfrost@gmail.com",
    license=read_contents("LICENSE"),
    packages=["micro"],
    package_data={"micro": ["assets/icon.png"]},
    install_requires=read_contents("requirements.txt").splitlines(),
    entry_points={"console_scripts": ["micro = micro.__main__:main"]},
    classifiers=[
        "Environment :: Console",
        "License :: GPL-3",
        "Operating System :: OS Independent",
    ],
)

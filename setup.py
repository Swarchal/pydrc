import os
from setuptools import setup


def read_requirements():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "requirements.txt")
    with open(path, "r") as f:
        requirements = [i.strip() for i in f.readlines()]
    return requirements


setup(
    name="pydrc",
    version="0.1.0",
    description="Dose reponse curve fitting",
    author="Scott Warchal",
    url="https://github.com/Swarchal/pydrc",
    packages=["pydrc"],
    install_requires=read_requirements(),
    tests_require="pytest",
    python_requires=">=3.8",
    zip_safe=True,
)

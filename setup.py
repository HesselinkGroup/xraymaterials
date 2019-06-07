from setuptools import find_packages
from setuptools import setup

requirements = ["pytest", "scipy", "numpy"]
version = "0.6.1"

setup(
    name="xraymaterials",
    version=version,
    author="Paul Hansen",
    description="X-ray material properties",
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements,
    python_requires=">=3",
)







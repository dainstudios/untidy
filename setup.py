from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="untidy",
    packages=["untidy"],
    version="0.0.1-alpha",
    license="MIT",
    description="Python package for creating messy data.",
    author="Paolo Fantinel, Sinem Unal Nazaroglu, Mate Varadi",
    author_email="paolo.fantinel@dainstudios.com, sinem.nazaroglu@dainstudios.com, mate.varadi@dainstudios.com",
    python_requires=">=3.8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dainstudios/untidy",
    install_requires=["pandas"],
    extras_require={"dev": ["pytest"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

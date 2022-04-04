from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

# Use requirements.txt to set the install_requires
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f]

# Use requirements-dev.txt and requirements-examples.txt to set the extras_require
extras_require = {}
with open("requirements-dev.txt") as f:
    extras_require["dev"] = [line.strip() for line in f]

with open("requirements-examples.txt") as f:
    extras_require["examples"] = [line.strip() for line in f]


setup(
    name="untidy",
    packages=["untidy"],
    version="0.0.1-alpha2",
    license="MIT",
    description="Python package for creating messy data.",
    author="Paolo Fantinel, Sinem Unal Nazaroglu, Mate Varadi",
    author_email="paolo.fantinel@dainstudios.com, sinem.nazaroglu@dainstudios.com, mate.varadi@dainstudios.com",
    python_requires=">=3.8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dainstudios/untidy",
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

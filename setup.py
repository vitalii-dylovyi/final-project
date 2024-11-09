from setuptools import setup, find_packages

setup(
    name="memok",
    version="0.0.1",
    py_modules=["memok"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "memok = src.main:main",
        ],
    },
)

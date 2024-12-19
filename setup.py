from setuptools import setup, find_packages

setup(
    name="pinit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pinit=pinit.initializer:main",
        ],
    },
    description="A simple tool to create venv and install packages.",
    author="Yasin Karbasi",
    author_email="yasinkardev@gmail.com",
    python_requires=">=3.12",
)

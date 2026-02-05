"""Setup configuration for Axilium."""

from setuptools import setup, find_packages

setup(
    name="axilium",
    version="1.0.0",
    description="A fun and engaging habit tracking desktop application",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "schedule>=1.2.0",
        "matplotlib>=3.7.0",
        "Pillow>=10.0.0",
        "plyer>=2.1.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "axilium=src.main:main",
        ],
    },
)

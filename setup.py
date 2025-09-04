"""
Setup script para el proyecto de automatización Zucarmex
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="zucarmex-automation",
    version="1.0.0",
    author="Zucarmex QA Team",
    author_email="qa@zucarmex.com",
    description="Sistema de automatización de pruebas para Credicam QA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zucarmex/automation-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zucarmex-test=run_tests:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.ini", "*.feature", "*.md"],
    },
)

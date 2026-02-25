"""
Setup configuration for Iconora Studio
Installation and distribution setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = (
    [line.strip() for line in requirements_file.read_text().splitlines() if line.strip()]
    if requirements_file.exists()
    else []
)

setup(
    name="Iconora-Studio",
    version="1.0.0",
    author="Iconora Team",
    author_email="support@iconora.com",
    description="Professional Windows application for image conversion and design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iconora-studio",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "iconora-studio=main:main",
        ],
    },
    extras_require={
        "dev": [
            "black>=24.1.1",
            "flake8>=7.0.0",
            "pylint>=3.0.3",
            "pytest>=7.4.4",
        ],
    },
    include_package_data=True,
    package_data={
        "assets": [
            "fonts/*",
            "icons/*",
            "templates/*",
        ],
    },
)

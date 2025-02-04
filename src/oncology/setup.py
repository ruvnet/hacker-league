"""
Setup script for oncology system package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="oncology",
    version="0.1.0",
    author="Roo",
    author_email="roo@example.com",
    description="Medical analysis system using LLMs and specialized tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/oncology",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "oncology=oncology.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "oncology": [
            "config/*.yaml",
            "tests/sample_data/*",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/oncology/issues",
        "Source": "https://github.com/yourusername/oncology",
        "Documentation": "https://oncology.readthedocs.io/",
    },
)
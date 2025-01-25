from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="insider-mirror",
    version="1.0.0",
    author="Roo Development Team",
    author_email="team@example.com",
    description="A sophisticated system for monitoring and mirroring publicly disclosed insider trades",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/insider-mirror",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "insider_mirror": [
            "config/*.yaml",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.8.0",
        "pandas>=2.1.0",
        "numpy>=1.21.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "finnhub-python>=2.4.0",
        "httpx>=0.24.0",
    ],
    entry_points={
        "console_scripts": [
            "insider-mirror=insider_mirror.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pylint>=2.17.0",
        ],
    },
)
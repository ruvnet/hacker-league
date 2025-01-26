from setuptools import setup, find_packages

setup(
    name="ruv-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "e2b-code-interpreter==0.1.8",
        "openrouter @ git+https://github.com/openrouter/openrouter-py.git@main",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "ruv=ruv_cli.cli:main",
        ],
    },
    python_requires=">=3.12",
    author="Your Name",
    author_email="your.email@example.com",
    description="RUV CLI - E2B Agent Management",
    long_description=open("e2b-agent/readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ruv-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)
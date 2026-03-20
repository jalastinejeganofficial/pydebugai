from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pydebugai",
    version="0.1.0",
    author="PyDebugAI Team",
    author_email="pydebugai@example.com",
    description="AI-powered Python debugging assistant — ChatGPT for Python errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydebugai/pydebugai",
    packages=find_packages(exclude=["tests*", "data*", "vscode-extension*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pydebugai=pydebugai.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pydebugai": ["data/*.json", "models/*.pkl"],
    },
)

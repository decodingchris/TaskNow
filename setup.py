from setuptools import setup, find_packages

setup(
    name="tasknow",
    version="1.0.0",
    description="Minimalist terminal task manager with single-task focus",
    long_description="""# TaskNow - Product Context

## Vision

A minimalist terminal task manager that helps users focus on one task at a time while still providing full task management capabilities.

## Core Features

- Single-task focus by default
- Simple command-based interface
- Full task list visibility when needed
- Completion tracking

## Technical Foundation

- Python implementation
- JSON data storage
- Ubuntu/Linux compatible

## User Workflow

1. User adds tasks with `tasknow add`
2. Views current task with `tasknow`
3. Marks completion with `tasknow done`
4. Manages full list with `tasknow list`/`tasknow remove` when needed
""",
    long_description_content_type="text/markdown",
    author="Decoding Chris",
    license="MIT",
    py_modules=["main"],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tasknow=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)
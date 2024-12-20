from setuptools import setup, find_packages

setup(
    name="preswald",                      # Your package name
    version="0.1.12",                      # Initial version
    author="Amrutha Gujjar",              # Author name
    author_email="amrutha@example.com",   # Author email
    description="A lightweight data workflow SDK.",  # Short description
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/StructuredLabs/preswald",  # GitHub repo URL
    license="Apache License 2.0",
    packages=find_packages(),             # Automatically find sub-packages
    classifiers=[                         # PyPI metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",              # Minimum Python version
    install_requires=[
        "pandas>=1.0.0",                  # Dependencies
        "requests>=2.0.0",
        "plotly>=5.0.0",
        "sqlalchemy>=1.4.0",
        "google-api-python-client>=2.0.0",
        "apscheduler>=3.0.0",
        "click>=8.0.0",
        "fastapi>=0.65.0",
        "uvicorn>=0.14.0",
        "pandas",
        "markdown",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "preswald=preswald.cli:cli",
        ]
    },
)

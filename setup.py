from setuptools import setup, find_packages

setup(
    name="preswald",                      # Your package name
    version="0.1.13",                      # Initial version
    author="Structured",              # Author name
    author_email="founders@structuredlabs.com",   # Author email
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
    python_requires=">=3.8,<3.13",              # Update Python version constraint
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.0.0",
        "plotly>=5.0.0",
        "sqlalchemy>=1.4.0",
        "google-api-python-client>=2.0.0",
        "apscheduler>=3.0.0",
        "click>=8.0.0",
        "fastapi>=0.65.0,<1.0.0",              # Add upper bound for stability
        "uvicorn>=0.14.0,<1.0.0",              # Add upper bound for stability
        "markdown>=3.0.0",                      # Add version constraint
        "jinja2>=3.0.0",                       # Add version constraint
    ],
    entry_points={
        "console_scripts": [
            "preswald=preswald.cli:cli",
        ]
    },
)

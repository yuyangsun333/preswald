from setuptools import setup, find_packages

setup(
    name="preswald",                      # Your package name
    version="0.1.0",                      # Initial version
    author="Amrutha Gujjar",              # Author name
    author_email="amrutha@example.com",   # Author email
    description="A lightweight data workflow SDK.",  # Short description
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/preswald",  # GitHub repo URL
    license="MIT",                        # License type
    packages=find_packages(),             # Automatically find sub-packages
    classifiers=[                         # PyPI metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
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
    ],
    entry_points={
        "console_scripts": [
            "preswald=preswald.cli:main",  # CLI command (if you have one)
        ]
    },
)

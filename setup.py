from setuptools import setup, find_packages

setup(
    name="pranomics",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "rich",
        "plotly",
    ],
    entry_points={
        "console_scripts": [
            "pranomics=pranomics.cli:main",
        ]
    },
    python_requires=">=3.10",
)


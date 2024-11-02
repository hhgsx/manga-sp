from setuptools import setup,find_packages

setup(
    name="manga-sp",
    version="0.0.1",
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "inquirer",
        "certifi",
        "pprintpp"
    ],
    entry_points={
        "console_scripts": [

        ]
    }
)
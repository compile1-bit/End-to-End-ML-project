from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    requirements =[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", " ") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Rossmann sales prediction",
    version="0.1.0",
    author="Esmael yasin",
    author_email="esmaelyasin89@gmail.com",
    description= " Predicting future sales for Rossmann stores using machine learning models and historical data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compile1-bit/rossamnn-sales-prediction.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires= get_requirements('requirements.txt')
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCBPE-luigiluz",
    version="0.0.1",
    author="Luigi Luz",
    author_email="luigiluz98@gmail.com",
    description="pyCBPE Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luigiluz/pyCBPE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
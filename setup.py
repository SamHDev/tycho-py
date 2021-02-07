import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name="tycho-py",
    version="0.1.0",
    author="SamHDev",
    author_email="sam.fucked.up@samh.dev",
    description="A python implementation of the Tycho binary format",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/samhdev/tychopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
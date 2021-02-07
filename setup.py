import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name="tycho-py",
    version="0.1.2",
    author="SamHDev",
    author_email="sam.fucked.up@samh.dev",
    description="A python implementation of the Tycho binary format",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/samhdev/tycho-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

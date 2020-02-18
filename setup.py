import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-Alex-quickcoder",
    version="0.0.1",
    author="Sobkovych Oleksandr",
    author_email="oleksandr.sobkovych@gmail.com",
    description="MovieWebMap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex-quickcoder/MovieWebMap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notAiess",
    version="0.1.0",
    author="Rendy Arya Kemal",
    author_email="rendyarya22@gmail.com",
    description="A Discord webhook for nomination feeds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rorre/notAiess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers"
    ],
)

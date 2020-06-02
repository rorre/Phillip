import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Phillip",
    version="0.2.0",
    author="Rendy Arya Kemal",
    author_email="rendyarya22@gmail.com",
    description="An event-driven for osu! feeds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rorre/Phillip",
    packages=['phillip', 'phillip.osu', 'phillip.osu.classes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
)

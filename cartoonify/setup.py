from distutils.core import setup

setup(
    # Application name:
    name="cartoonify",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Dan Macnish",

    # Packages
    packages=["app"],

    # todo fill out manifest.in
    # Include additional files into the package
    include_package_data=True,

    #
    # license="LICENSE.txt",
    description="Python package for turning a photo into a cartoon.",

    # long_description=open("README.txt").read(),
    # todo add dependent packages
    # Dependent packages (distributions)
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        cartoonify=run:run
    ''',
)
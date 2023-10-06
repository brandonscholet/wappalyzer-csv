from setuptools import setup, find_packages

setup(
    name='wappybird',
    version='0.3.6',
    description='Wappalyzer CLI tool to find Web Technologies ',
    author='Brandon',
    author_email='brandon@scholet.net',
    url='https://github.com/brandonscholet/wappybird',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'requests',
        'colorama',
    ],
	entry_points={
        'console_scripts': [
            'wappybird = wappybird.main:do_the_thing',
        ],
    },
    package_data={
        'wappybird': ['technologies.json'],  # Specify the path to your JSON file
    },
    include_package_data=True,  # Include package data when building the distribution
)

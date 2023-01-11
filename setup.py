from setuptools import *

if __name__ == "__main__":

    f = open("requirements.txt", 'r')

    dependencies = f.read().splitlines()

    f.close()

    setup(
    scripts = ["src/wappy"],
    name='wappybird',
    version='0.2.4',
    packages=find_packages(),
    install_requires=[
        dependencies
    ],
    
    
    )

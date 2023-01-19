from setuptools import setup, find_packages

if __name__ == "__main__":

    with open("requirements.txt") as f:
        dependencies = f.readlines()

    setup(
        test/no-ref/forking-practice
        scripts=["src/wappy"],
        name='wappybird',
        version='0.3.4',
        packages=find_packages(),
        install_requires=[dep.strip() for dep in dependencies],
    )

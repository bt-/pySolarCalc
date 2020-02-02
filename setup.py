from setuptools import setup

setup(
    name='pySolarCalc',
    url='http://github.com/bt-/pySolarCalc',
    license='GPLv3',
    author='Ben Taylor and Gage Gallagher',
    python_requires='>=3.7',
    install_requires=['param>=1.9'],
    author_email='benjaming.taylor@gmail.com',
    description=('A tool for cable and conduit sizing calculations\
                  following the NEC.'),
    # packages=['captest'],
    # include_package_data=True,
    platforms='any',
)

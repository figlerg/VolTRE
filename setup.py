from setuptools import setup, find_packages

setup(
    name='VolTRE',
    version='0.1.0',
    packages=find_packages(include=['parse', 'sample', 'volume', 'match', 'misc', 'probabilistic']),
    url='https://github.com/figlerg/VolTRE',
    license='BSD 3-Clause License',
    author='Felix Gigler, Benoît Barbot, Ezio Bartocci, Nicolas Basset, Thao Dang, Dejan Nickovic',
    author_email='felix.n.gigler@gmail.com',
    description='Volumetry and uniform sampling methods for timed regular expressions. '
)

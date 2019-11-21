import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='CoverageCalculatorPy',
    version='1.0.0',
    author='Chris Medway',
    scripts= ['CoverageCalculatorPy.py'],
    author_email='josephhalstead89@gmail.com',
    description='Calculated coverage metrics from a GATK3 Depth Of Coverage file and a bedfile  ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AWGL/CoverageCalculatorPy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
   'pytabix>=0.1',
],
)
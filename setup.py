from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='testalizer',
    version='0.1.0',
    description='Programm for testing cortex analyzers',
    long_description=long_description,
    url='https://github.com/3c7/testalizer',
    author='Nils Kuhnert',
    license='AGPL-3.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console'
    ],
    keywords='computer emergency response team cert dfir statistic statistics misp intelmq',
    packages=find_packages(),
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'testalizer=testalizer.testalizer:entrypoint'
        ]
    }
)

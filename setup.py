from setuptools import setup

setup(name='nhsbt_acquire',
    version='0.1a',
    description='Acquire and store NHSBT blood & platelet levels',
    url='https://github.com/svenlatham/nhsbt-blood-levels/',
    license='MIT',
    author='Sven Latham',
    author_email='sven@svenlatham.com',
    packages=['nhsbt_acquire'],
    entry_points={
        'console_scripts': ['nhsbt_acquire=nhsbt_acquire.cli:main'],
    }
)
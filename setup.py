from setuptools import setup

setup(
    name='PunOfTheDayBot',
    version='1.0',
    packages=[],
    url='',
    license='MIT',
    author='alanspringfield',
    author_email='',
    description='A Reddit bot that responds to comments containing "!pun" with a random pun from punoftheday.com',
    install_requires=['praw', 'requests']
)

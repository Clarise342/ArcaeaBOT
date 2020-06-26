import pathlib
import re
import subprocess

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

with open(ROOT / 'requirements.txt', 'r', encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name='arcaea',
    author='Clarise342',
    url='https://github.com/Clarise342/discordpy-startup',

    license='MIT LICENSE',
    description='Arcaea',
    project_urls={
        'Code': 'https://github.com/Clarise342/discordpy-startup',
        'Issue tracker': 'https://github.com/Starwort/discord.gui/issues'
    },

    version='1.0.0',
    packages=['discordpy-startup'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires='>=3.6.0',

    keywords='discord.gui discord.py discord cog gui extension',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ]
)


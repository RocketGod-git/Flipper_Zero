import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dora',
    version='1.0.0',
    author='Siddharth Dushantha',
    author_email='siddharth.dushantha@gmail.com',
    description='Find exposed API keys based on RegEx and get exploitation methods for some of keys that are found',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sdushantha/dora',
    packages=setuptools.find_packages(),
    package_data={'dora': ['db/*']},
    entry_points={
        'console_scripts': [
            'dora=dora.__main__:main',
        ]
    },
    install_requires=['colorama~=0.4']
)

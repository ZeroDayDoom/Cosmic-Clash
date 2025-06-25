from setuptools import setup, find_packages

setup(
    name='RewGames',
    version='1.0',
    packages=find_packages(),
    install_requires=['pygame', 'time', 'random'],
    author='Ankit Rewar',
    author_email='ankitreawar001@gmail.com',
    description='This is a fun game made by me using pygame library from python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/myfile',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

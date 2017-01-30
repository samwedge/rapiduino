from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='rapiduino',

    version='0.1.0',

    description='Rapidly develop code to control an Arduino using Python',
    long_description='Rapidly develop code to control an Arduino using Python. Python code is executed on a computer. '
                     'The Arduino is controlled through serial connection. Suitable for rapid development where a '
                     'computer connection is not a burden, or where a small microcomputer (such as a Raspberry Pi) '
                     'can be used.',

    url='https://github.com/samwedge/rapiduino',

    author='Sam Wedge',
    author_email='samwedge@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='arduino python rapid development serial communication',

    packages=find_packages(exclude=['arduino', 'tests']),

    install_requires=['serial', 'six'],

    extras_require={
        'test': ['mock'],
    },

    package_data={

    },

    data_files=[],

    entry_points={

    },
)

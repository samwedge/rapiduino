from setuptools import setup, find_packages
from os import path
import rapiduino

here = path.abspath(path.dirname(__file__))

install_requires = [
    'pyserial==3.4',
]

extras_require = {
    'dev': [
        'flake8==3.7.9',
        'wheel==0.33.6',
        'setuptools==45.1.0',
        'twine==3.1.1',
    ],
    'travis': [
        'coveralls==1.10.0',
    ]
}
extras_require['travis'] += extras_require['dev']

with open('README.md') as f:
    long_description = f.read()

setup(
    name='rapiduino',
    version=rapiduino.__version__,
    description='Rapidly develop code to control an Arduino using Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/samwedge/rapiduino',
    author='Sam Wedge',
    author_email='samwedge@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='arduino python rapid development serial communication',
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={},
    data_files=[],
    entry_points={}
)

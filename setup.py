from os import path
import codecs
from setuptools import setup, find_packages

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

tests_require = [
    'Django==1.11.11',
    'nose==1.3.7',
    'mock==2.0.0',
    'httpretty==0.8.14',
    'sure==1.4.7',
    'coveralls',
]

setup(
    name='django-twitter-tag',
    version='1.1',
    author='Ilya Baryshev',
    author_email='baryshev@gmail.com',
    packages=find_packages(exclude="tests"),
    url='https://github.com/coagulant/django-twitter-tag',
    license='MIT',
    description="A django template tag to display user's recent tweets.",
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    install_requires=[
        "django-classy-tags==0.8.0",
        "twitter==1.18.0",
        "django-appconf==1.0.2",
        'six==1.11.0',
    ],
    tests_require=tests_require,
    test_suite="nose.collector",
    extras_require={'test': tests_require},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)

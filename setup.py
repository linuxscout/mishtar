#! /usr/bin/python
from setuptools import setup

# to install type:
# python setup.py install --root=/
def readme():
    with open('README.rst') as f:
        return f.read()
        
setup (name='mishtar', version='0.1',
      author='Taha Zerrouki',
      author_email='taha_zerrouki@hotmail.com',
      url='http://pypi.python.com/projects/mishtar/',
      license='GPL',
      description="Mishtar: Arabic text chuncker, temporal and named entities extraction",
      long_description = readme(),
      package_dir={'mishtar': 'mishtar',},
      packages=['mishtar'],
       install_requires=["pyarabic>=0.6.2",
      ],
      package_data = {
        'pyarabic': ['doc/*.*','doc/html/*'],
        },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Natural Language :: Arabic',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Linguistic',
          ],
    );


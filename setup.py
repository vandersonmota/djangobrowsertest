from setuptools import setup, find_packages
import sys, os
 
version = '0.1'
 
 
setup(name='djangobrowsertest',
      version=version,
      description="django browser testing that lets the programmer choose which test tool he'll use",
      long_description='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='browser django python test',
      author='Vanderson Mota',
      author_email='vanderson.mota@gmail.com',
      url='http://github.com/vandersonmota/django-browsertest',
      license='MIT License',
      packages=['djangobrowsertest', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['django',],
      entry_points="",
      )
 
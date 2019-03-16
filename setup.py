#!/usr/bin/env python

from distutils.core import setup

setup(name='insta_tag_search',
      version='0.1',
      description='',
      author='Drex',
      author_email='aeturnum@gmail.com',
      packages=['insta_tag_search'],
      license="MIT",
      install_requires=["InstagramApi", "openpyxl"],
      entry_points={
              'console_scripts': [
                  'instahash = insta_tag_search.run:get_hashtags',
                  'instatag = insta_tag_search.run:get_usertags',
              ],
          }
     )

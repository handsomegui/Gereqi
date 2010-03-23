#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from distutils.core import setup 

setup (name='Gereqi', 
            version='0.3.6', 
            description='An Amarok-1.4 clone in PyQt4 and Gstreamer', 
            author='Jon Noble',
            author_email='jonnobleuk@gmail.com', 
            url='http://github.com/regomodo/Gereqi', 
            license='GPLv3', 
            packages=['gereqi'], 
            package_data={'gereqi': ['gereqi/*.py']}, 
            scripts = ["bin/Gereqi"]
            )

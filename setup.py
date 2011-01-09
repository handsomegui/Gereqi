#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from distutils.core import setup 

setup(name='gereqi', 
        version='0.5.0', 
        description='A music organiser and player.', 
        author='Jonathan Noble',
        author_email='jonnobleuk@gmail.com', 
        url='http://github.com/regomodo/Gereqi', 
        license='GPLv3', 
        packages=['gereqi','gereqi.devices', 'gereqi.icons','gereqi.audio',
                  'gereqi.information','gereqi.storage'], 
        package_data={
                      'gereqi': ['gereqi/*.py'],
                      'gereqi.devices': ['gereqi/devices/*.py'],
                      'gereqi.icons': ['gereqi/icons/*.py'],
                      'gereqi.audio': ['gereqi/audio/*.py'],
                      'gereqi.storage': ['gereqi/storage/*.py'],
                      'gereqi.information': ['gereqi/information/*.py']
                      }, 
        
        data_files=[('/usr/share/applications',['gereqi/data/gereqi.desktop']),
            ('/usr/share/pixmaps',['gereqi/data/gereqi.png'])],
        scripts = ["bin/gereqi"]
        )

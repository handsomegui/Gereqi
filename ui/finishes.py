#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import Qt


class Finishes:
    def __init__(self):
        return
    
    def set_lyrics(self, lyr):
        self.tabWidget_2.setTabEnabled(1, True)
        print lyr
        
    def set_cover(self, img):
        cover = QPixmap()
        cover = cover.fromImage(img)
        cover = cover.fromImage(img)
        cover = cover.scaledToWidth(200, Qt.SmoothTransformation)
        self.coverView.setPixmap(cover)        
        
    def set_wiki(self, html):
        self.tabWidget_2.setTabEnabled(2, True)
        self.wikiView.setHtml(str(html))
        
    def finish_build(self, status):
        if str(status) == "finished":
            print "Scanned directory."
            self.stat_bttn.setEnabled(False)
            self.stat_prog.setToolTip("Finished")
            self.stat_prog.setValue(100)
            self.collectTree.clear()
            self.setup_db_tree()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QFont, QMenu, QTreeWidgetItem, QShortcut, \
QKeySequence, QLabel, QProgressBar, QToolButton, QIcon, QPixmap, \
QAction, QSystemTrayIcon, qApp, QDirModel
from PyQt4.QtCore import QString, SIGNAL, QSize, SLOT, QDir


class Setups:
    """
    This deals with the initialisation of the Ui
    and various dynamic widgets.
    """
    def __init__(self):
        return
        
    def init_setups(self):
        self.setup_db_tree()
        self.__setup_shortcuts()
        self.__setup_extra()        
        self.__create_actions()        
        self.__playlist_add_menu()
        self.__create_tray_menu()
        self.__setup_fileview()
        self.__disable_tabs()
    
    def __playlist_add_menu(self):
        """
        In the 'playlist' tab a menu is required for
        the 'add' button
        """
        menu = QMenu(self)
        playlist_menu = QMenu(self)
        playlist_menu.setTitle(QString("Playlist"))
        new = QAction(self.tr("New..."), self)
        existing = QAction(self.tr("Import Existing..."), self)
        playlist_menu.addAction(new)
        playlist_menu.addAction(existing)        
        menu.addMenu(playlist_menu)
        smart = QAction(self.tr("Smart Playlist..."), self)
        dynamic = QAction(self.tr("Dynamic Playlist..."), self)
        radio = QAction(self.tr("Radio Stream..."), self)
        podcast = QAction(self.tr("Podcast..."), self)
        menu.addAction(smart)
        menu.addAction(dynamic)
        menu.addAction(radio)
        menu.addAction(podcast)
        self.addPlylstBttn.setMenu(menu)
        #TODO: add functions for actions
    
    def __setup_shortcuts(self):
        """
        Keyboard shortcuts setup
        """
        delete = QShortcut(QKeySequence(self.tr("Del")), self)
        self.connect(delete, SIGNAL("activated()"), self.del_track) 
        
    def __setup_extra(self):
        """
        Extra __init__ things to add to the UI
        """        
        self.progSldr.setPageStep(0)
        self.progSldr.setSingleStep(0)
        self.stat_lbl = QLabel("Finished")
        self.stat_prog = QProgressBar()
        self.stat_bttn = QToolButton()
        self.play_type_bttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        self.stat_prog.setRange(0, 100)
        self.stat_prog.setValue(100)
        self.stat_prog.setMaximumSize(QSize(100, 18))
        self.stat_bttn.setIcon(icon)
        self.stat_bttn.setAutoRaise(True)
        self.stat_bttn.setEnabled(False)
        self.play_type_bttn.setText("N")
        self.play_type_bttn.setCheckable(True)
        self.play_type_bttn.setAutoRaise(True)
        self.statusBar.addPermanentWidget(self.stat_lbl)
        self.statusBar.addPermanentWidget(self.stat_prog)
        self.statusBar.addPermanentWidget(self.stat_bttn)
        self.statusBar.addPermanentWidget(self.play_type_bttn)
        # Headers for the Playlist widget
        # TODO: dynamic columns at some point
        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), \
                   self.tr("Album"), self.tr("Year"), self.tr("Genre"),   \
                   self.tr("Length"), self.tr("Bitrate"), self.tr("FileName")]
        for val in range(len(headers)):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)
        
    def __setup_fileview(self):
        """
        A fileView browser where tracks can be (eventually)
        added to the playlist
        """
            
        self.dir_model = QDirModel()
        filters = QDir.Files | QDir.AllDirs | QDir.Readable | QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        #FIXME: do not hard code file formats
        self.dir_model.setNameFilters(["*.ogg","*.flac","*.mp3"])
        self.fileView.setModel(self.dir_model)
        self.fileView.setColumnHidden(1, True)
        self.fileView.setColumnHidden(2, True)
        self.fileView.setColumnHidden(3, True)
        self.fileView.expandToDepth(0)
        self.connect(self.fileView, SIGNAL("expanded (const QModelIndex&)"), \
                                                      self.__resize_fileview) 
        self.connect(self.fileView, SIGNAL("doubleClicked (const QModelIndex&)"), self.__fileview_item)
        
    def __resize_fileview(self):
        """
        Resizes the fileView to it's contents.
        Because of the '0' this seperate method is needed
        """
        self.fileView.resizeColumnToContents(0)
        
    def __fileview_item(self, index):
        """
        This takes the fileview item and deduces whether
        it's a file or directory and populates playlist if possible
        """
        if self.dir_model.isDir(index):
            fname = self.dir_model.filePath(index)
            searcher = QDir(fname)
            searcher.setFilter(QDir.Files)
            searcher.setFilter(QDir.Files)
            # FIXME: do not hard code formats
            searcher.setNameFilters(["*.ogg","*.flac","*.mp3"])
            for item in searcher.entryInfoList():
                fname = item.absoluteFilePath()
                self.add2playlist(self.extras.qstr2uni(fname))
        else:
            fname = self.dir_model.filePath(index)
            self.add2playlist(self.extras.qstr2uni(fname))
        
    def __create_actions(self):
        #TODO: get rid of this. Put actions and connects in own function
        # to reduce the number of unneeded pointers
        
        #FIXME: the linking to non-existing methods has to be bad
        # These playing actions are from the toolbar.
        self.connect(self.actionPlay, SIGNAL("toggled ( bool )"), self.playBttn, SLOT("setChecked(bool)"))
        self.connect(self.actionNext_Track, SIGNAL("triggered()"), self.nxtBttn, SLOT("click()"))
        self.connect(self.actionPrevious_Track, SIGNAL("triggered()"), self.prevBttn, SLOT("click()"))  
        self.connect(self.actionStop, SIGNAL("triggered()"), self.stopBttn, SLOT("click()"))
        self.connect(self.play_type_bttn, SIGNAL('toggled ( bool )'), self.__play_type)
        self.connect(self.stat_bttn, SIGNAL("pressed()"), self.quit_build)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        quit_action = QAction(self.tr("&Quit"), self)
        self.play_action = QAction(self.tr("&Play"), self)
        next_action = QAction(self.tr("&Next"), self)
        prev_action = QAction(self.tr("&Previous"), self)
        stop_action = QAction(self.tr("&Stop"), self)
        self.play_action.setCheckable(True)
        self.view_action = QAction(self.tr("&Visible"), self)
        self.view_action.setCheckable(True)
        self.view_action.setChecked(True)
        tray_icon_menu = QMenu(self)
        icon = QIcon(QPixmap(":/Icons/app.png"))
        tray_icon_menu.addAction(icon, QString("Gereqi"))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(prev_action)
        tray_icon_menu.addAction(self.play_action)
        tray_icon_menu.addAction(stop_action)
        tray_icon_menu.addAction(next_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.view_action)
        tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        icon2 = QIcon(QPixmap(":/Icons/app-paused.png"))
        self.tray_icon.setIcon(icon2)
        self.tray_icon.setContextMenu(tray_icon_menu)
        self.connect(self.play_action, SIGNAL("toggled(bool)"), self.playBttn, SLOT("setChecked(bool)"))
        self.connect(next_action, SIGNAL("triggered()"), self.nxtBttn, SLOT("click()"))
        self.connect(prev_action, SIGNAL("triggered()"), self.prevBttn, SLOT("click()"))
        self.connect(stop_action, SIGNAL("triggered()"), self.stopBttn, SLOT("click()"))
        self.connect(self.view_action, SIGNAL("toggled(bool)"), self.minimise_to_tray)  
        self.connect(quit_action, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.connect(self.tray_icon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.tray_event)
        self.tray_icon.show()
        self.tray_icon.setToolTip("Stopped")       
        
    def setup_db_tree(self, filt=None):
        """
        viewing the media database in the QTreeView
        """
        #TODO: make the creation aware of the collectTimeBox widget
        time_filter = self.collectTimeBox.currentIndex()
        self.collectTree.clear()
        # This gives multiples of the same thing i.e albums
        artists = self.media_db.get_artists()
        artists = sorted(artists)
        old_char = None
        char = None
        font = QFont()
        font.setBold(True)
        for cnt in range(len(artists)):
            artist = artists[cnt][0]
            # When creating collection tree only 
            #  allow certain artists based on the filter.
            if filt and (filt.lower() not in artist.lower()):
                continue
            char = artist[0]   
            if char != old_char:
                old_char = char  
                char = QTreeWidgetItem(["== %s ==" % char])
                char.setFont(0, font)
                self.collectTree.addTopLevelItem(char)
            artist = QTreeWidgetItem([QString(artist)])
            artist.setChildIndicatorPolicy(0)
            self.collectTree.addTopLevelItem(artist)
            
    def __play_type(self, checked):
        if checked:
            self.play_type_bttn.setText("R")
        else:
            self.play_type_bttn.setText("N")

    def __disable_tabs(self):
        self.contentTabs.setTabEnabled(1, False)
        self.contentTabs.setTabEnabled(2, False)
        self.parentTabs.setTabEnabled(2, False)
        self.parentTabs.setTabEnabled(3, False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QFont, QMenu, QTreeWidgetItem, QShortcut, \
QKeySequence, QLabel, QProgressBar, QToolButton, QIcon, QPixmap, \
QAction, QSystemTrayIcon, qApp, QTreeView, QDirModel, QHBoxLayout, \
QHeaderView
from PyQt4.QtCore import QStringList, QString, SIGNAL, QSize, SLOT, QDir
from Ui_interface import Ui_MainWindow
from gstbe import Player


class Setups(Ui_MainWindow):
    """
    This deals with the initialisation of the Ui
    and various dynamic widgets.
    """
    def __init__(self):
        super(Setups, self).__init__()
        
    def init_setups(self):
        self.setup_db_tree()
        self.setup_shortcuts()
        self.setup_extra()        
        self.create_actions()        
        self.playlist_add_menu()
        self.create_tray_menu()
        self.setup_fileview()
        self.setup_pipeline()
        
    def setup_pipeline(self):
        self.playbin = Player()
        self.connect(self.playbin, SIGNAL("tick ( int )"), self.prog_tick)
        self.playbin.pipe_line.connect("about-to-finish",  self.about_to_finish)
        self.connect(self.playbin, SIGNAL("track_changed()"), self.track_changed)
        self.connect(self.playbin, SIGNAL("finished()"), self.finished_playing)
    
    def playlist_add_menu(self):
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
    
    def setup_shortcuts(self):
        """
        Keyboard shortcuts setup
        """
        delete = QShortcut(QKeySequence(self.tr("Del")), self)
        self.connect(delete, SIGNAL("activated()"), self.del_track) 
        
    def setup_extra(self):
        """
        Extra __init__ things to add to the UI
        """
        self.tabWidget_2.setTabEnabled(1, False)
        self.tabWidget_2.setTabEnabled(2, False)
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
        
    def setup_fileview(self):
        """
        A fileView browser where tracks can be (eventually)
        added to the playlist
        """
        model = QDirModel()
        filters = QDir.Files | QDir.Dirs | QDir.Readable | QDir.NoDotAndDotDot
        model.setFilter(filters)
        model.setReadOnly(True)
        self.fileView.setModel(model)
        self.fileView.setColumnHidden(1, True)
        self.fileView.setColumnHidden(2, True)
        self.fileView.setColumnHidden(3, True)

    def create_actions(self):
        #TODO: get rid of this. Put actions and connects in own function
        # to reduce the number of unneeded pointers
        
        # These playing actions are from the toolbar.
        self.connect(self.actionPlay, SIGNAL("toggled(bool)"), self.playBttn.setChecked) 
        self.connect(self.actionNext_Track, SIGNAL("triggered()"), self.on_nxtBttn_pressed)
        self.connect(self.actionPrevious_Track, SIGNAL("triggered()"), self.on_prevBttn_pressed)  
        self.connect(self.actionStop, SIGNAL("triggered()"), self.on_stopBttn_pressed)
        self.connect(self.play_type_bttn, SIGNAL('toggled(bool)'), self.play_type)
        self.connect(self.cover_thread, SIGNAL("Activated ( QImage ) "), self.set_cover) # Linked to QThread
        self.connect(self.html_thread, SIGNAL("Activated ( QString ) "), self.set_wiki)
        self.connect(self.build_db_thread, SIGNAL("Activated ( int ) "), self.stat_prog.setValue)
        self.connect(self.build_db_thread, SIGNAL("Activated ( QString ) "), self.finish_build)
        self.connect(self.stat_bttn, SIGNAL("pressed()"), self.quit_build)
        
    def create_tray_menu(self):
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
        icon = QIcon(QPixmap(":/Icons/drawing.png"))
        tray_icon_menu.addAction(icon, QString("Gereqi"))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(prev_action)
        tray_icon_menu.addAction(self.play_action)
        tray_icon_menu.addAction(stop_action)
        tray_icon_menu.addAction(next_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.view_action)
        tray_icon_menu.addAction(quit_action)
        # No. This icon isn't final. Just filler.
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setContextMenu(tray_icon_menu)
        self.connect(self.play_action, SIGNAL("toggled(bool)"), self.playBttn.setChecked)
        self.connect(next_action, SIGNAL("triggered()"), self.on_nxtBttn_pressed)
        self.connect(prev_action, SIGNAL("triggered()"), self.on_prevBttn_pressed)
        self.connect(stop_action, SIGNAL("triggered()"), self.on_stopBttn_pressed)
        self.connect(self.view_action, SIGNAL("toggled(bool)"), self.minimise_to_tray)  
        self.connect(quit_action, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.connect(self.tray_icon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.tray_event)
        self.tray_icon.show()       
        
    def setup_db_tree(self, filt=None):
        """
        viewing the media database in the QTreeView
        """
        #TODO: make the creation aware of the collectTimeBox widget
        time_filter = self.collectTimeBox.currentIndex()
        #Because we now call this to filter, we need to clear the collecttree
        # before changing it
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
            # When creating collection tree only allow certain 
            # artists based on the filter.
            if filt:
                filt = filt.lower()
                art = artist.lower()
                if filt not in art:
                    continue
            try:
                char = artist[0]
            except:
                char = ""            
            if char != old_char:
                old_char = char  
                char = "== %s ==" % char
                char = QStringList(char)
                char = QTreeWidgetItem(char)
                char.setFont(0, font)
                self.collectTree.addTopLevelItem(char)
            artist = QString(artist)
            artist = QStringList(artist)
            artist = QTreeWidgetItem(artist)
            artist.setChildIndicatorPolicy(0)
            self.collectTree.addTopLevelItem(artist)

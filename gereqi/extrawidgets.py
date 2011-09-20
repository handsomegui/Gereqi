# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import QWebPage

import time
import devices
import icons.configuration
from storage.Collection import CollectionDb
from icons.configuration import MyIcons
from playlist.Auto import Unplayed,Top

import extraneous
    

class SetupExtraWidgets:
    """
    This should be done before the main ui is shown
    e.g. on app initialisation
    """
    def __init__(self, parent):
        self.ui = parent        
        self.ui.track_tbl.horizontalHeader().setMovable(True)
        
        self.__setup_filesystem_tree()
        self.__create_tray_menu()
        
        self.__setup_misc()
        self.__key_shortcuts()
        # Load all the button/action icons
        icons.configuration.Setup(self.ui)
        
    def __setup_filesystem_tree(self):
        """
        A filesystem_tree browser where tracks can be (eventually)
        added to the playlist
        """
        self.ui.dir_model = QDirModel()
        filters = QDir.Files|QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.ui.dir_model.setFilter(filters)
        self.ui.dir_model.setReadOnly(True)
        self.ui.dir_model.setNameFilters(self.ui.format_filter)
        self.ui.filesystem_tree.setModel(self.ui.dir_model) 
        self.ui.filesystem_tree.setColumnHidden(1, True)
        self.ui.filesystem_tree.setColumnHidden(2, True)
        self.ui.filesystem_tree.setColumnHidden(3, True)
        self.ui.filesystem_tree.expandToDepth(0)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        icons = MyIcons()
        quit_action = QAction(icons.icon("quit"), "&Quit", self.ui)
        self.ui.play_action = QAction(icons.icon("play"), "&Play", self.ui)
        next_action = QAction(icons.icon("next"), "&Next", self.ui)
        prev_action = QAction(icons.icon("back"), "&Previous", self.ui)
        stop_action = QAction(icons.icon("stop"), "&Stop", self.ui)
        
        self.ui.play_action.setCheckable(True)
        self.ui.view_action = QAction("&Visible", self.ui)
        self.ui.view_action.setCheckable(True)
        self.ui.view_action.setChecked(True)
        tray_menu = QMenu(self.ui)
        tray_menu.addAction(QIcon(":/application/app.png"), "Gereqi")
        tray_menu.addSeparator()
        tray_menu.addAction(prev_action)
        tray_menu.addAction(self.ui.play_action)
        tray_menu.addAction(stop_action)
        tray_menu.addAction(next_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.ui.view_action)
        tray_menu.addAction(quit_action)
        self.ui.tray_icon = QSystemTrayIcon(self.ui)
        self.ui.tray_icon.setIcon(QIcon(":/application/paused.png"))
        self.ui.tray_icon.setContextMenu(tray_menu)
        self.ui.tray_icon.setToolTip("Stopped")    
        
        self.ui.play_action.toggled.connect(self.ui.play_bttn.setChecked)
        self.ui.view_action.toggled.connect(self.ui.minimise_to_tray)
        self.ui.tray_icon.activated.connect(self.ui.tray_event)
        next_action.triggered.connect(self.ui.next_bttn.click)
        prev_action.triggered.connect(self.ui.prev_bttn.click)
        stop_action.triggered.connect(self.ui.stop_bttn.click)
        quit_action.triggered.connect(self.ui.shutdown)     
       
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """
        icons = MyIcons()
        self.ui.stat_lbl = QLabel("Finished")
        self.ui.stat_prog = QProgressBar()
        
        self.ui.stat_prog.setRange(0, 100)
        self.ui.stat_prog.setValue(100)
        self.ui.stat_prog.setMaximumSize(QSize(100, 18))
        
        
        self.ui.stat_bttn = QToolButton()
        self.ui.stat_bttn.setIcon(icons.icon("quit"))
        self.ui.stat_bttn.setAutoRaise(True)
        self.ui.stat_bttn.setEnabled(False)
        
        self.ui.play_type_bttn = QToolButton()  
        self.ui.play_type_bttn.setCheckable(True)
        self.ui.play_type_bttn.setAutoRaise(True)
        self.ui.play_type_bttn.setIcon(QIcon(":/application/normal.png"))
        
        self.ui.statusBar.addPermanentWidget(self.ui.stat_lbl)
        self.ui.statusBar.addPermanentWidget(self.ui.stat_prog)
        self.ui.statusBar.addPermanentWidget(self.ui.stat_bttn)
        self.ui.statusBar.addPermanentWidget(self.ui.play_type_bttn)
        # Headers for the Playlist widget
        headers = ["Track", "Title", "Artist",
                  "Album", "Year", "Genre",  
                   "Length", "Bitrate", "FileName"]
        for val in range(len(headers)):
            self.ui.track_tbl.insertColumn(val)
        self.ui.track_tbl.setHorizontalHeaderLabels(headers)
      
        # Disables the webView link-clicks as we want to manually handle them
        self.ui.info_view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.ui.wiki_view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.ui.info_view.setRenderHint(QPainter.HighQualityAntialiasing)


    def __key_shortcuts(self):
        """
        various keyboard shortcuts 
        """
        # remove the selected track from the playlist
        delete = QShortcut(QKeySequence("Del"), self.ui)
        delete.activated.connect(self.ui.playlisting.del_tracks)

        

class WidgetManips:
    """
    For repeated custom widget actions
    """
    def __init__(self, parent):
        parent.track_tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        parent.track_tbl.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        
        parent.track_tbl.customContextMenuRequested.connect(self.__context_menu)
        parent.track_tbl.horizontalHeader().customContextMenuRequested.connect(self.__header_menu)
        parent.vertical_tabs.currentChanged.connect(self.__tab_changed)
        parent.play_type_bttn.toggled.connect(self.__play_mode_changed)
        self.__hdr_menu_setup()
        self.ui = parent
        self.dev_man = None
        
#        self.mydel = MyDelegate()
#        self.mydel.mode = "artist"
#        self.ui.collect_tree.setItemDelegate(self.mydel)
#        self.ui.collect_tree.setUniformRowHeights(False)
#        self.ui.collect_tree.setIconSize(QSize(46,46))        
        
        self.threader = AlbumItem()
        self.threader.new_item.connect(self.__add_album_item)
        
        
    def __play_mode_changed(self, check):
        """
        Changes the icon of the random mode button depending
        if checked or not
        """
        if check:
            icon = ":/application/random.png"
        else:
            icon = ":/application/normal.png"            
        self.ui.play_type_bttn.setIcon(QIcon(icon))
        
        
    def __add_from_dev(self, item):
        self.__dev_view_expand(item)
        par = item.parent()
        if not par:
            art = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art)
            # List comps or generators are very,very flakey
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui.playlisting.add_to_playlist(trk,info)
            return
        
        par_par = par.parent()
        if not par_par:
            art = str(par.text(0))
            alb = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art,album=alb)
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui.playlisting.add_to_playlist(trk,info)
                
        else:
            artist = str(par_par.text(0))
            album = str(par.text(0))
            title = str(item.text(0))
            track = self.dev_interface.filename(artist, album, title)
            info = self.dev_interface.metadata(track)
            self.ui.playlisting.add_to_playlist(track,info)
        
    def __dev_view_expand(self,item):
        par = item.parent()
        if not par:
            artist = str(item.text(0))
            if item.childCount() > 0:
                return
            albums = self.dev_interface.albums(artist)
            for alb in albums:
                now = QTreeWidgetItem([alb])
                now.setChildIndicatorPolicy(0)
                item.addChild(now)
            return
            
        elif not par.parent():
            artist = str(par.text(0))
            album = str(item.text(0))
            if item.childCount() > 0:
                return
            
            tracks = self.dev_interface.tracks(artist,album)
            for trk in tracks:
                now = QTreeWidgetItem([trk])
                now.setChildIndicatorPolicy(1)
                item.addChild(now)
            return
        
    def __hdr_menu_setup(self):
        """
            Setup the Context Menu for the table headers.
            Needed to keep the checkbox states
        """        
        self.hdr_menu = QMenu()
        hdrs = ["Track","Title","Artist","Album","Year","Genre","Length",
                "Bitrate","FileName"]
        for hdr in hdrs:
            action = self.hdr_menu.addAction(hdr)
            action.setCheckable(True)
            action.setChecked(True)
        
    def __header_menu(self,pos): 
        """
            The names of each header column is checkable
            for viewing of its column
        """
        action = self.hdr_menu.exec_(self.ui.track_tbl.horizontalHeader().mapToGlobal(pos))
        hdr_pos = self.ui.playlisting.header_search(action.iconText())
        hdr_view = False if action.isChecked() else True
        self.ui.track_tbl.setColumnHidden(hdr_pos,hdr_view)
        
    def __tab_changed(self,pos):
        if (pos == 4):
            if not self.dev_man:
                self.dev_man = devices.Devices()
                
            self.ui.connect_dev.clicked.connect(self.__mount_dev)
            self.ui.disconnect_dev.clicked.connect(self.__umount_dev)
            self.ui.device_view.itemExpanded.connect(self.__dev_view_expand)
            self.ui.device_view.itemDoubleClicked.connect(self.__add_from_dev)
            for dev in self.dev_man.device_list:
                self.ui.devices_box.addItem(dev["PATH"])
                
                
    def __pop_dev_view(self):
        """
            Populate the treeView based on the
            currently mounted device
        """
        arts = self.dev_interface.artists()
        for art in arts:
            row = QTreeWidgetItem([art])
            row.setChildIndicatorPolicy(0)
            self.ui.device_view.addTopLevelItem(row)
        
    def __ipod_view(self,m_point):
        """
            Shows the iPods contents in the treeview
        """
        self.ui.device_view.clear()
        self.dev_interface = devices.Ipod(m_point)
        self.__pop_dev_view()
        
    def __mount_dev(self):
        """
            Mount the device shown in the combobox
        """
        dev_now = str(self.ui.devices_box.currentText())
        m_point = self.dev_man.mount(dev_now)
        self.ui.connect_dev.setEnabled(False)
        self.ui.disconnect_dev.setEnabled(True)
        for dev in self.dev_man.device_list:
            if (dev["PATH"] != dev_now):
                continue
            
            dev["MOUNTPOINT"] = m_point
            if (dev["PROTOCOL"] == "ipod"):
                self.__ipod_view(m_point)
                return
        
    def __umount_dev(self):
        """
            Unmount current device
        """
        dev = str(self.ui.devices_box.currentText())
        self.dev_man.unmount(dev)
        self.ui.device_view.clear()
        self.ui.disconnect_dev.setEnabled(False)
        self.ui.connect_dev.setEnabled(True)
        
    def __context_menu(self,pos):
        # do nothing if table is empty
        if self.ui.track_tbl.rowCount() > 0:
            rows = []
            
            for r in self.ui.track_tbl.selectedItems():
                r_now = self.ui.track_tbl.row(r)
                if r_now not in rows:
                    rows.append(r_now)
                    
                    
            item_now = self.ui.track_tbl.itemAt(pos)
            #The coulmn we clicked in
            col_now = self.ui.track_tbl.column(item_now)
            tag_name = self.ui.track_tbl.horizontalHeaderItem(col_now).text()
            
            menu = QMenu()
            icon = QIcon().fromTheme("media-playback-start")
            play_action = menu.addAction(icon, "Play")
            menu.addSeparator()
            
            remove_action = menu.addAction("Remove From Playlist")
            
            menu.addSeparator()
            
            icon = QIcon().fromTheme("document-open")
            manage_menu = QMenu("Manage File")
            manage_menu.setIcon(icon)
            manage_organise = manage_menu.addAction("Organise File")
            manage_delete = manage_menu.addAction("Delete File")
            
            menu.addMenu(manage_menu)
            
            icon = QIcon().fromTheme("edit-copy", QIcon(":/icon/edit-copy.png"))
            # Can't change these aspects of the file
            copy_tags_action = menu.addAction(icon, "Copy Tags to Clipboard")
            if tag_name not in ["FileName","Length", "Bitrate"]:
                edit_tag = menu.addAction("Edit Tag '%s'" % tag_name)
            
            action = menu.exec_(self.ui.track_tbl.mapToGlobal(pos))
            if not action:
                return
                        
            row = item_now.row()
            
            if action == play_action:
                # Stop playback then start again 
                self.ui.play_bttn.setChecked(False)
                self.ui.play_bttn.setChecked(True)
                
            # Honestly, I have no idea what use this is. 
            # At least it's easy to implement
            elif action == copy_tags_action:
                row = self.ui.track_tbl.itemAt(pos).row()
                col = self.ui.playlisting.header_search("Title")
                tag = self.ui.track_tbl.item(row,col).text()
                clip = QApplication.clipboard()
                clip.setText(tag)
                
            elif action == remove_action:
                self.ui.playlisting.del_track(row)
                
            elif action == manage_organise:
                print "ORGANISE?"
                
            elif action == manage_delete:
                print "YEAH, I'M NOT DELETING"
                
            elif action == edit_tag:
                text = QInputDialog.getText(None, tag_name,
                                         "Change the tag to:",
                                         QLineEdit.Normal,
                                         item_now.text())
                
                if text[1]:
                    col = self.ui.playlisting.header_search("FileName")
                    for row in rows:                        
                        fname = self.ui.track_tbl.item(row,col).text()
                        self.ui.media_db.update_tag(fname,tag_name.lower(),text[0])
                        self.ui.track_tbl.item(row,col_now).setText(text[0])
                

    def __add_album_item(self,item):
        row = QTreeWidgetItem([item[0]])
        row.setIcon(0,QIcon(item[1]))
        row.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        self.ui.collect_tree.addTopLevelItem(row)
        
    def time_filter_value(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.ui.collect_time_box.currentIndex()
        calc = lambda val: int(round(time.time() - val))
        now = time.localtime()
        today = ((now[3] * 60) +  now[4] ) * 60 + now[5]
        filts = [today, 604800, 2629743, 7889229, 31556926]   
        if index > 0:
            return calc(filts[index - 1])
        else:
            return 0
            
    def pop_playlist_view(self):
        """
        Populates the playlist listview
        """
        font = QFont()
        font.setBold(True)        
        self.ui.playlist_tree.clear()
        playlists = self.ui.media_db.playlist_list()
        headers = ["Playlists","Auto"]       
        
        for item in headers:
            hdr = QTreeWidgetItem([item])
            hdr.setIcon(0,QIcon(":/application/files.png")) 
            hdr.setFont(0, font)
            hdr.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
         
            if item == "Playlists":
                for play in playlists:
                    now = QTreeWidgetItem([play])
                    now.setIcon(0,QIcon(MyIcons().icon("folder")))
                    hdr.addChild(now)
                    tracks = self.ui.media_db.playlist_tracks(play)
                    for track in tracks:
                        info = self.ui.media_db.get_info(track)
                        if info is not None:
                            now.addChild(QTreeWidgetItem(["%s - %s" %
                                         (info["title"], info["artist"]) ]))
            #TODO: make dynamic e.g. populate on open of playlist
            # instead of program load                
            if item == "Auto":
                hdr.addChild(Top())
                hdr.addChild(Unplayed())
                                                                                     
            self.ui.playlist_tree.addTopLevelItem(hdr)
                
    def icon_change(self, state):
        """
        Depending on the specific state of the program
        the play button's icon will vary
        """
        icons = MyIcons()
        if state == "play":
            icon = icons.icon("pause")
            tray = QIcon(":/application/app.png")
        elif state == "pause":            
            icon = icons.icon("play")
            tray = QIcon(":/application/paused.png")

        self.ui.play_bttn.setIcon(icon)
        self.ui.tray_icon.setIcon(tray)
        
        
        
class AlbumItem(QThread):
    new_item = pyqtSignal(tuple)
    def __init__(self,parent=None):
        QThread.__init__(self)
        self.db = CollectionDb("album_items")
        self.exiting = False
    
    def __del__(self):
        self.exiting = True
        self.wait()
            
    def stop(self):
        self.exiting = True
        
    def set_values(self,time_filt, filter):
        self.exiting = False  
        self.filter = filter
        self.time_filt = time_filt
    
    def run(self):
        self.exiting = False
        extras = extraneous.Extraneous()
        for item in self.db.get_albums_all(self.time_filt, self.filter):
            if self.exiting:
                break       
            cover = extras.get_cover_source(item['artist'],item['album'],True, False)
            if not cover:
                cover = ":icons/nocover.png"
            else:
                cover = cover.replace("file://", '')
            self.new_item.emit((item['album'],cover))


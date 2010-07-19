# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jon/Documents/Projects/Gereqi/gereqi/interface.ui'
#
# Created: Mon Jul 19 22:41:07 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 533)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setMargin(2)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.vertical_tabs = QtGui.QTabWidget(self.splitter)
        self.vertical_tabs.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vertical_tabs.sizePolicy().hasHeightForWidth())
        self.vertical_tabs.setSizePolicy(sizePolicy)
        self.vertical_tabs.setMinimumSize(QtCore.QSize(280, 0))
        self.vertical_tabs.setMaximumSize(QtCore.QSize(600, 16777215))
        self.vertical_tabs.setTabPosition(QtGui.QTabWidget.West)
        self.vertical_tabs.setDocumentMode(True)
        self.vertical_tabs.setObjectName("vertical_tabs")
        self.contentTab = QtGui.QWidget()
        self.contentTab.setObjectName("contentTab")
        self.gridLayout_2 = QtGui.QGridLayout(self.contentTab)
        self.gridLayout_2.setMargin(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontal_tabs = QtGui.QTabWidget(self.contentTab)
        self.horizontal_tabs.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontal_tabs.sizePolicy().hasHeightForWidth())
        self.horizontal_tabs.setSizePolicy(sizePolicy)
        self.horizontal_tabs.setMinimumSize(QtCore.QSize(250, 0))
        self.horizontal_tabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.horizontal_tabs.setUsesScrollButtons(False)
        self.horizontal_tabs.setDocumentMode(True)
        self.horizontal_tabs.setTabsClosable(False)
        self.horizontal_tabs.setMovable(False)
        self.horizontal_tabs.setObjectName("horizontal_tabs")
        self.musicTab = QtGui.QWidget()
        self.musicTab.setObjectName("musicTab")
        self.gridLayout_12 = QtGui.QGridLayout(self.musicTab)
        self.gridLayout_12.setMargin(2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.info_view = QtWebKit.QWebView(self.musicTab)
        self.info_view.setAcceptDrops(False)
        self.info_view.setToolTip("None")
        self.info_view.setWhatsThis("None")
        self.info_view.setUrl(QtCore.QUrl("about:blank"))
        self.info_view.setObjectName("info_view")
        self.gridLayout_12.addWidget(self.info_view, 0, 0, 1, 1)
        self.horizontal_tabs.addTab(self.musicTab, "")
        self.wikipediaTab = QtGui.QWidget()
        self.wikipediaTab.setObjectName("wikipediaTab")
        self.gridLayout_4 = QtGui.QGridLayout(self.wikipediaTab)
        self.gridLayout_4.setMargin(2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.wiki_view = QtWebKit.QWebView(self.wikipediaTab)
        self.wiki_view.setAutoFillBackground(True)
        self.wiki_view.setStyleSheet("")
        self.wiki_view.setUrl(QtCore.QUrl("about:blank"))
        self.wiki_view.setZoomFactor(1.0)
        self.wiki_view.setObjectName("wiki_view")
        self.gridLayout_4.addWidget(self.wiki_view, 0, 0, 1, 1)
        self.horizontal_tabs.addTab(self.wikipediaTab, "")
        self.gridLayout_2.addWidget(self.horizontal_tabs, 0, 1, 1, 1)
        self.vertical_tabs.addTab(self.contentTab, "")
        self.collectionTab = QtGui.QWidget()
        self.collectionTab.setObjectName("collectionTab")
        self.gridLayout_3 = QtGui.QGridLayout(self.collectionTab)
        self.gridLayout_3.setMargin(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clear_collect_bttn = QtGui.QToolButton(self.collectionTab)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/edit-clear-locationbar-ltr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_collect_bttn.setIcon(icon1)
        self.clear_collect_bttn.setIconSize(QtCore.QSize(24, 24))
        self.clear_collect_bttn.setAutoRaise(True)
        self.clear_collect_bttn.setObjectName("clear_collect_bttn")
        self.horizontalLayout.addWidget(self.clear_collect_bttn)
        self.search_collect_edit = QtGui.QLineEdit(self.collectionTab)
        self.search_collect_edit.setObjectName("search_collect_edit")
        self.horizontalLayout.addWidget(self.search_collect_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.collect_time_box = QtGui.QComboBox(self.collectionTab)
        self.collect_time_box.setMaxVisibleItems(6)
        self.collect_time_box.setMaxCount(6)
        self.collect_time_box.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.collect_time_box.setFrame(True)
        self.collect_time_box.setObjectName("collect_time_box")
        self.collect_time_box.addItem("")
        self.collect_time_box.addItem("")
        self.collect_time_box.addItem("")
        self.collect_time_box.addItem("")
        self.collect_time_box.addItem("")
        self.collect_time_box.addItem("")
        self.verticalLayout_2.addWidget(self.collect_time_box)
        self.collect_tree = QtGui.QTreeWidget(self.collectionTab)
        self.collect_tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.collect_tree.setProperty("showDropIndicator", False)
        self.collect_tree.setAlternatingRowColors(True)
        self.collect_tree.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.collect_tree.setIndentation(15)
        self.collect_tree.setRootIsDecorated(True)
        self.collect_tree.setUniformRowHeights(True)
        self.collect_tree.setAnimated(True)
        self.collect_tree.setExpandsOnDoubleClick(False)
        self.collect_tree.setObjectName("collect_tree")
        self.verticalLayout_2.addWidget(self.collect_tree)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.vertical_tabs.addTab(self.collectionTab, "")
        self.playlistsTab = QtGui.QWidget()
        self.playlistsTab.setObjectName("playlistsTab")
        self.gridLayout_6 = QtGui.QGridLayout(self.playlistsTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.line_2 = QtGui.QFrame(self.playlistsTab)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)
        self.rename_playlist_bttn = QtGui.QToolButton(self.playlistsTab)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/edit-rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rename_playlist_bttn.setIcon(icon2)
        self.rename_playlist_bttn.setIconSize(QtCore.QSize(24, 24))
        self.rename_playlist_bttn.setAutoRaise(True)
        self.rename_playlist_bttn.setObjectName("rename_playlist_bttn")
        self.horizontalLayout_5.addWidget(self.rename_playlist_bttn)
        self.delete_playlist_bttn = QtGui.QToolButton(self.playlistsTab)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_playlist_bttn.setIcon(icon3)
        self.delete_playlist_bttn.setIconSize(QtCore.QSize(24, 24))
        self.delete_playlist_bttn.setAutoRaise(True)
        self.delete_playlist_bttn.setObjectName("delete_playlist_bttn")
        self.horizontalLayout_5.addWidget(self.delete_playlist_bttn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.playlist_tree = QtGui.QTreeWidget(self.playlistsTab)
        self.playlist_tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.playlist_tree.setProperty("showDropIndicator", False)
        self.playlist_tree.setObjectName("playlist_tree")
        self.verticalLayout_5.addWidget(self.playlist_tree)
        self.gridLayout_6.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.vertical_tabs.addTab(self.playlistsTab, "")
        self.filesTab = QtGui.QWidget()
        self.filesTab.setObjectName("filesTab")
        self.gridLayout_13 = QtGui.QGridLayout(self.filesTab)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.filesystem_tree = QtGui.QTreeView(self.filesTab)
        self.filesystem_tree.setIndentation(15)
        self.filesystem_tree.setExpandsOnDoubleClick(False)
        self.filesystem_tree.setObjectName("filesystem_tree")
        self.gridLayout_13.addWidget(self.filesystem_tree, 0, 0, 1, 1)
        self.vertical_tabs.addTab(self.filesTab, "")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.clear_trktbl_bttn = QtGui.QToolButton(self.layoutWidget)
        self.clear_trktbl_bttn.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/edit-clear-list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_trktbl_bttn.setIcon(icon4)
        self.clear_trktbl_bttn.setIconSize(QtCore.QSize(24, 24))
        self.clear_trktbl_bttn.setAutoRaise(True)
        self.clear_trktbl_bttn.setObjectName("clear_trktbl_bttn")
        self.horizontalLayout_4.addWidget(self.clear_trktbl_bttn)
        self.save_trktbl_bttn = QtGui.QToolButton(self.layoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Icons/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_trktbl_bttn.setIcon(icon5)
        self.save_trktbl_bttn.setIconSize(QtCore.QSize(24, 24))
        self.save_trktbl_bttn.setAutoRaise(True)
        self.save_trktbl_bttn.setObjectName("save_trktbl_bttn")
        self.horizontalLayout_4.addWidget(self.save_trktbl_bttn)
        self.prev_trktbl_bttn = QtGui.QToolButton(self.layoutWidget)
        self.prev_trktbl_bttn.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Icons/edit-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev_trktbl_bttn.setIcon(icon6)
        self.prev_trktbl_bttn.setIconSize(QtCore.QSize(24, 24))
        self.prev_trktbl_bttn.setAutoRaise(True)
        self.prev_trktbl_bttn.setObjectName("prev_trktbl_bttn")
        self.horizontalLayout_4.addWidget(self.prev_trktbl_bttn)
        self.next_trktbl_bttn = QtGui.QToolButton(self.layoutWidget)
        self.next_trktbl_bttn.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Icons/edit-redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_trktbl_bttn.setIcon(icon7)
        self.next_trktbl_bttn.setIconSize(QtCore.QSize(24, 24))
        self.next_trktbl_bttn.setAutoRaise(True)
        self.next_trktbl_bttn.setObjectName("next_trktbl_bttn")
        self.horizontalLayout_4.addWidget(self.next_trktbl_bttn)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.clear_search_bttn = QtGui.QToolButton(self.layoutWidget)
        self.clear_search_bttn.setIcon(icon1)
        self.clear_search_bttn.setIconSize(QtCore.QSize(24, 24))
        self.clear_search_bttn.setAutoRaise(True)
        self.clear_search_bttn.setObjectName("clear_search_bttn")
        self.horizontalLayout_4.addWidget(self.clear_search_bttn)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.search_trktbl_edit = QtGui.QLineEdit(self.layoutWidget)
        self.search_trktbl_edit.setMinimumSize(QtCore.QSize(200, 0))
        self.search_trktbl_edit.setObjectName("search_trktbl_edit")
        self.horizontalLayout_4.addWidget(self.search_trktbl_edit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.track_tbl = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.track_tbl.sizePolicy().hasHeightForWidth())
        self.track_tbl.setSizePolicy(sizePolicy)
        self.track_tbl.setMinimumSize(QtCore.QSize(400, 0))
        self.track_tbl.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.track_tbl.setProperty("showDropIndicator", False)
        self.track_tbl.setDragEnabled(True)
        self.track_tbl.setDragDropOverwriteMode(False)
        self.track_tbl.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.track_tbl.setAlternatingRowColors(True)
        self.track_tbl.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.track_tbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.track_tbl.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.track_tbl.setShowGrid(False)
        self.track_tbl.setGridStyle(QtCore.Qt.DashLine)
        self.track_tbl.setWordWrap(False)
        self.track_tbl.setCornerButtonEnabled(True)
        self.track_tbl.setObjectName("track_tbl")
        self.track_tbl.setColumnCount(0)
        self.track_tbl.setRowCount(0)
        self.track_tbl.horizontalHeader().setVisible(True)
        self.track_tbl.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.track_tbl)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prev_bttn = QtGui.QToolButton(self.layoutWidget)
        self.prev_bttn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Icons/media-skip-backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev_bttn.setIcon(icon8)
        self.prev_bttn.setIconSize(QtCore.QSize(24, 24))
        self.prev_bttn.setAutoRaise(True)
        self.prev_bttn.setObjectName("prev_bttn")
        self.horizontalLayout_3.addWidget(self.prev_bttn)
        self.play_bttn = QtGui.QToolButton(self.layoutWidget)
        self.play_bttn.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Icons/media-playback-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_bttn.setIcon(icon9)
        self.play_bttn.setIconSize(QtCore.QSize(24, 24))
        self.play_bttn.setCheckable(True)
        self.play_bttn.setAutoRaise(True)
        self.play_bttn.setObjectName("play_bttn")
        self.horizontalLayout_3.addWidget(self.play_bttn)
        self.stop_bttn = QtGui.QToolButton(self.layoutWidget)
        self.stop_bttn.setEnabled(False)
        self.stop_bttn.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Icons/media-playback-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_bttn.setIcon(icon10)
        self.stop_bttn.setIconSize(QtCore.QSize(24, 24))
        self.stop_bttn.setAutoRaise(True)
        self.stop_bttn.setObjectName("stop_bttn")
        self.horizontalLayout_3.addWidget(self.stop_bttn)
        self.next_bttn = QtGui.QToolButton(self.layoutWidget)
        self.next_bttn.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/Icons/media-skip-forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_bttn.setIcon(icon11)
        self.next_bttn.setIconSize(QtCore.QSize(24, 24))
        self.next_bttn.setAutoRaise(True)
        self.next_bttn.setObjectName("next_bttn")
        self.horizontalLayout_3.addWidget(self.next_bttn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.mute_bttn = QtGui.QToolButton(self.layoutWidget)
        self.mute_bttn.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/Icons/audio-volume-high.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mute_bttn.setIcon(icon12)
        self.mute_bttn.setIconSize(QtCore.QSize(24, 24))
        self.mute_bttn.setCheckable(True)
        self.mute_bttn.setAutoRaise(True)
        self.mute_bttn.setObjectName("mute_bttn")
        self.horizontalLayout_3.addWidget(self.mute_bttn)
        self.volume_sldr = QtGui.QSlider(self.layoutWidget)
        self.volume_sldr.setMaximumSize(QtCore.QSize(200, 200))
        self.volume_sldr.setMaximum(100)
        self.volume_sldr.setProperty("value", 100)
        self.volume_sldr.setOrientation(QtCore.Qt.Horizontal)
        self.volume_sldr.setInvertedAppearance(False)
        self.volume_sldr.setInvertedControls(False)
        self.volume_sldr.setTickPosition(QtGui.QSlider.NoTicks)
        self.volume_sldr.setObjectName("volume_sldr")
        self.horizontalLayout_3.addWidget(self.volume_sldr)
        self.volume_lbl = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_lbl.sizePolicy().hasHeightForWidth())
        self.volume_lbl.setSizePolicy(sizePolicy)
        self.volume_lbl.setMinimumSize(QtCore.QSize(24, 0))
        self.volume_lbl.setObjectName("volume_lbl")
        self.horizontalLayout_3.addWidget(self.volume_lbl)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progress_sldr = QtGui.QSlider(self.layoutWidget)
        self.progress_sldr.setMaximum(0)
        self.progress_sldr.setOrientation(QtCore.Qt.Horizontal)
        self.progress_sldr.setObjectName("progress_sldr")
        self.horizontalLayout_2.addWidget(self.progress_sldr)
        self.progress_lbl = QtGui.QLabel(self.layoutWidget)
        self.progress_lbl.setObjectName("progress_lbl")
        self.horizontalLayout_2.addWidget(self.progress_lbl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 792, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuActions = QtGui.QMenu(self.menuBar)
        self.menuActions.setObjectName("menuActions")
        self.menuPlaylist = QtGui.QMenu(self.menuBar)
        self.menuPlaylist.setObjectName("menuPlaylist")
        self.menuCurrent = QtGui.QMenu(self.menuPlaylist)
        self.menuCurrent.setObjectName("menuCurrent")
        self.menuSettings = QtGui.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuMode = QtGui.QMenu(self.menuBar)
        self.menuMode.setObjectName("menuMode")
        self.menuRepeat = QtGui.QMenu(self.menuMode)
        self.menuRepeat.setObjectName("menuRepeat")
        self.menuRandom = QtGui.QMenu(self.menuMode)
        self.menuRandom.setObjectName("menuRandom")
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionConfigure = QtGui.QAction(MainWindow)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionRescan_Collection = QtGui.QAction(MainWindow)
        self.actionRescan_Collection.setObjectName("actionRescan_Collection")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.play_media_actn = QtGui.QAction(MainWindow)
        self.play_media_actn.setObjectName("play_media_actn")
        self.minimise_tray_actn = QtGui.QAction(MainWindow)
        self.minimise_tray_actn.setCheckable(True)
        self.minimise_tray_actn.setChecked(True)
        self.minimise_tray_actn.setObjectName("minimise_tray_actn")
        self.actionClear_Current = QtGui.QAction(MainWindow)
        self.actionClear_Current.setObjectName("actionClear_Current")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClear = QtGui.QAction(MainWindow)
        self.actionClear.setIcon(icon4)
        self.actionClear.setObjectName("actionClear")
        self.actionSave_2 = QtGui.QAction(MainWindow)
        self.actionSave_2.setIcon(icon5)
        self.actionSave_2.setObjectName("actionSave_2")
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionUpdate_Collection = QtGui.QAction(MainWindow)
        self.actionUpdate_Collection.setObjectName("actionUpdate_Collection")
        self.actionAbout_Gereqi = QtGui.QAction(MainWindow)
        self.actionAbout_Gereqi.setObjectName("actionAbout_Gereqi")
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionRptOff = QtGui.QAction(MainWindow)
        self.actionRptOff.setCheckable(True)
        self.actionRptOff.setChecked(True)
        self.actionRptOff.setObjectName("actionRptOff")
        self.actionRptTrack = QtGui.QAction(MainWindow)
        self.actionRptTrack.setCheckable(True)
        self.actionRptTrack.setObjectName("actionRptTrack")
        self.actionRptAlbum = QtGui.QAction(MainWindow)
        self.actionRptAlbum.setCheckable(True)
        self.actionRptAlbum.setObjectName("actionRptAlbum")
        self.actionRptPlaylist = QtGui.QAction(MainWindow)
        self.actionRptPlaylist.setCheckable(True)
        self.actionRptPlaylist.setObjectName("actionRptPlaylist")
        self.actionRndOff = QtGui.QAction(MainWindow)
        self.actionRndOff.setCheckable(True)
        self.actionRndOff.setChecked(True)
        self.actionRndOff.setObjectName("actionRndOff")
        self.actionRndTrack = QtGui.QAction(MainWindow)
        self.actionRndTrack.setCheckable(True)
        self.actionRndTrack.setObjectName("actionRndTrack")
        self.actionRndAlbum = QtGui.QAction(MainWindow)
        self.actionRndAlbum.setCheckable(True)
        self.actionRndAlbum.setObjectName("actionRndAlbum")
        self.actionFavor = QtGui.QAction(MainWindow)
        self.actionFavor.setObjectName("actionFavor")
        self.play_cd_actn = QtGui.QAction(MainWindow)
        self.play_cd_actn.setObjectName("play_cd_actn")
        self.prev_track_actn = QtGui.QAction(MainWindow)
        self.prev_track_actn.setObjectName("prev_track_actn")
        self.play_actn = QtGui.QAction(MainWindow)
        self.play_actn.setCheckable(True)
        self.play_actn.setObjectName("play_actn")
        self.stop_actn = QtGui.QAction(MainWindow)
        self.stop_actn.setObjectName("stop_actn")
        self.actionNext_Track = QtGui.QAction(MainWindow)
        self.actionNext_Track.setObjectName("actionNext_Track")
        self.actionEqualiser = QtGui.QAction(MainWindow)
        self.actionEqualiser.setObjectName("actionEqualiser")
        self.menuActions.addAction(self.play_media_actn)
        self.menuActions.addAction(self.play_cd_actn)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.minimise_tray_actn)
        self.menuActions.addAction(self.prev_track_actn)
        self.menuActions.addAction(self.play_actn)
        self.menuActions.addAction(self.stop_actn)
        self.menuActions.addAction(self.actionNext_Track)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionQuit)
        self.menuCurrent.addAction(self.actionClear)
        self.menuCurrent.addAction(self.actionSave_2)
        self.menuCurrent.addAction(self.actionLoad)
        self.menuPlaylist.addAction(self.menuCurrent.menuAction())
        self.menuSettings.addAction(self.actionConfigure)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Gereqi)
        self.menuRepeat.addAction(self.actionRptOff)
        self.menuRepeat.addAction(self.actionRptTrack)
        self.menuRepeat.addAction(self.actionRptAlbum)
        self.menuRepeat.addAction(self.actionRptPlaylist)
        self.menuRandom.addAction(self.actionRndOff)
        self.menuRandom.addAction(self.actionRndTrack)
        self.menuRandom.addAction(self.actionRndAlbum)
        self.menuRandom.addSeparator()
        self.menuRandom.addAction(self.actionFavor)
        self.menuMode.addAction(self.menuRepeat.menuAction())
        self.menuMode.addAction(self.menuRandom.menuAction())
        self.menuTools.addAction(self.actionEqualiser)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionUpdate_Collection)
        self.menuTools.addAction(self.actionRescan_Collection)
        self.menuBar.addAction(self.menuActions.menuAction())
        self.menuBar.addAction(self.menuPlaylist.menuAction())
        self.menuBar.addAction(self.menuMode.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.label.setBuddy(self.search_trktbl_edit)

        self.retranslateUi(MainWindow)
        self.vertical_tabs.setCurrentIndex(1)
        self.horizontal_tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.volume_sldr, QtCore.SIGNAL("valueChanged(int)"), self.volume_lbl.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Gereqi", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontal_tabs.setTabText(self.horizontal_tabs.indexOf(self.musicTab), QtGui.QApplication.translate("MainWindow", "Music", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontal_tabs.setTabText(self.horizontal_tabs.indexOf(self.wikipediaTab), QtGui.QApplication.translate("MainWindow", "Wikipedia", None, QtGui.QApplication.UnicodeUTF8))
        self.vertical_tabs.setTabText(self.vertical_tabs.indexOf(self.contentTab), QtGui.QApplication.translate("MainWindow", "Context", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_collect_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear Search Field", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_collect_bttn.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.search_collect_edit.setToolTip(QtGui.QApplication.translate("MainWindow", "Enter search terms here", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(0, QtGui.QApplication.translate("MainWindow", "Entire Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(1, QtGui.QApplication.translate("MainWindow", "Added Today", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(2, QtGui.QApplication.translate("MainWindow", "Added Within 1 Week", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(3, QtGui.QApplication.translate("MainWindow", "Added Within 1 Month", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(4, QtGui.QApplication.translate("MainWindow", "Added Within 3 Months", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_time_box.setItemText(5, QtGui.QApplication.translate("MainWindow", "Added Within 1 Year", None, QtGui.QApplication.UnicodeUTF8))
        self.collect_tree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Artist/Album", None, QtGui.QApplication.UnicodeUTF8))
        self.vertical_tabs.setTabText(self.vertical_tabs.indexOf(self.collectionTab), QtGui.QApplication.translate("MainWindow", "Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.rename_playlist_bttn.setText(QtGui.QApplication.translate("MainWindow", "_", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_playlist_bttn.setText(QtGui.QApplication.translate("MainWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.playlist_tree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.vertical_tabs.setTabText(self.vertical_tabs.indexOf(self.playlistsTab), QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.vertical_tabs.setTabText(self.vertical_tabs.indexOf(self.filesTab), QtGui.QApplication.translate("MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_trktbl_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_trktbl_bttn.setText(QtGui.QApplication.translate("MainWindow", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.save_trktbl_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Save Playlist As", None, QtGui.QApplication.UnicodeUTF8))
        self.save_trktbl_bttn.setText(QtGui.QApplication.translate("MainWindow", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.prev_trktbl_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.prev_trktbl_bttn.setText(QtGui.QApplication.translate("MainWindow", "P", None, QtGui.QApplication.UnicodeUTF8))
        self.next_trktbl_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.next_trktbl_bttn.setText(QtGui.QApplication.translate("MainWindow", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_search_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear search field", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_search_bttn.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.search_trktbl_edit.setToolTip(QtGui.QApplication.translate("MainWindow", "Playlist Search", None, QtGui.QApplication.UnicodeUTF8))
        self.track_tbl.setSortingEnabled(True)
        self.prev_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Previous Track", None, QtGui.QApplication.UnicodeUTF8))
        self.play_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Play/Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.stop_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.next_bttn.setToolTip(QtGui.QApplication.translate("MainWindow", "Next Track", None, QtGui.QApplication.UnicodeUTF8))
        self.volume_sldr.setToolTip(QtGui.QApplication.translate("MainWindow", "Volume Control", None, QtGui.QApplication.UnicodeUTF8))
        self.volume_lbl.setText(QtGui.QApplication.translate("MainWindow", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.progress_lbl.setText(QtGui.QApplication.translate("MainWindow", "00:00 | 00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("MainWindow", "Engage", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlaylist.setTitle(QtGui.QApplication.translate("MainWindow", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.menuCurrent.setTitle(QtGui.QApplication.translate("MainWindow", "Current", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMode.setTitle(QtGui.QApplication.translate("MainWindow", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRepeat.setTitle(QtGui.QApplication.translate("MainWindow", "Repeat", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRandom.setTitle(QtGui.QApplication.translate("MainWindow", "Random", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure Gereqi", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRescan_Collection.setText(QtGui.QApplication.translate("MainWindow", "Rescan Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.play_media_actn.setText(QtGui.QApplication.translate("MainWindow", "Play Media", None, QtGui.QApplication.UnicodeUTF8))
        self.play_media_actn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.minimise_tray_actn.setText(QtGui.QApplication.translate("MainWindow", "Visible", None, QtGui.QApplication.UnicodeUTF8))
        self.minimise_tray_actn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Current.setText(QtGui.QApplication.translate("MainWindow", "Clear Current", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_2.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate_Collection.setText(QtGui.QApplication.translate("MainWindow", "Update Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Gereqi.setText(QtGui.QApplication.translate("MainWindow", "About  Gereqi", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRptOff.setText(QtGui.QApplication.translate("MainWindow", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRptTrack.setText(QtGui.QApplication.translate("MainWindow", "Track", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRptAlbum.setText(QtGui.QApplication.translate("MainWindow", "Album", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRptPlaylist.setText(QtGui.QApplication.translate("MainWindow", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRndOff.setText(QtGui.QApplication.translate("MainWindow", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRndTrack.setText(QtGui.QApplication.translate("MainWindow", "Track", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRndAlbum.setText(QtGui.QApplication.translate("MainWindow", "Albums", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFavor.setText(QtGui.QApplication.translate("MainWindow", "Favor", None, QtGui.QApplication.UnicodeUTF8))
        self.play_cd_actn.setText(QtGui.QApplication.translate("MainWindow", "Play Audio CD", None, QtGui.QApplication.UnicodeUTF8))
        self.prev_track_actn.setText(QtGui.QApplication.translate("MainWindow", "Previous Track", None, QtGui.QApplication.UnicodeUTF8))
        self.play_actn.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.stop_actn.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext_Track.setText(QtGui.QApplication.translate("MainWindow", "Next Track", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEqualiser.setText(QtGui.QApplication.translate("MainWindow", "Equaliser", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import icons.resource_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jon/Documents/projects/amaroq/ui/amaroq.ui'
#
# Created: Fri Apr 17 17:06:46 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 710)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_8 = QtGui.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_9 = QtGui.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.tabWidget_2.addTab(self.tab_9, "")
        self.gridLayout_2.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clrBttn = QtGui.QToolButton(self.tab_2)
        self.clrBttn.setObjectName("clrBttn")
        self.horizontalLayout.addWidget(self.clrBttn)
        self.srchEdt = QtGui.QLineEdit(self.tab_2)
        self.srchEdt.setObjectName("srchEdt")
        self.horizontalLayout.addWidget(self.srchEdt)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.collectTree = QtGui.QTreeWidget(self.tab_2)
        self.collectTree.setObjectName("collectTree")
        self.verticalLayout_2.addWidget(self.collectTree)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prevBttn = QtGui.QToolButton(self.centralWidget)
        self.prevBttn.setObjectName("prevBttn")
        self.horizontalLayout_3.addWidget(self.prevBttn)
        self.playBttn = QtGui.QToolButton(self.centralWidget)
        self.playBttn.setCheckable(True)
        self.playBttn.setObjectName("playBttn")
        self.horizontalLayout_3.addWidget(self.playBttn)
        self.stopBttn = QtGui.QToolButton(self.centralWidget)
        self.stopBttn.setObjectName("stopBttn")
        self.horizontalLayout_3.addWidget(self.stopBttn)
        self.nxtBttn = QtGui.QToolButton(self.centralWidget)
        self.nxtBttn.setObjectName("nxtBttn")
        self.horizontalLayout_3.addWidget(self.nxtBttn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.volSldr = QtGui.QSlider(self.centralWidget)
        self.volSldr.setMaximumSize(QtCore.QSize(200, 200))
        self.volSldr.setMaximum(100)
        self.volSldr.setProperty("value", QtCore.QVariant(100))
        self.volSldr.setOrientation(QtCore.Qt.Horizontal)
        self.volSldr.setInvertedAppearance(False)
        self.volSldr.setInvertedControls(False)
        self.volSldr.setTickPosition(QtGui.QSlider.NoTicks)
        self.volSldr.setObjectName("volSldr")
        self.horizontalLayout_3.addWidget(self.volSldr)
        self.volLbl = QtGui.QLabel(self.centralWidget)
        self.volLbl.setObjectName("volLbl")
        self.horizontalLayout_3.addWidget(self.volLbl)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progSldr = QtGui.QSlider(self.centralWidget)
        self.progSldr.setOrientation(QtCore.Qt.Horizontal)
        self.progSldr.setObjectName("progSldr")
        self.horizontalLayout_2.addWidget(self.progSldr)
        self.progLbl = QtGui.QLabel(self.centralWidget)
        self.progLbl.setObjectName("progLbl")
        self.horizontalLayout_2.addWidget(self.progLbl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.playlistTree = QtGui.QTableWidget(self.centralWidget)
        self.playlistTree.setObjectName("playlistTree")
        self.playlistTree.setColumnCount(0)
        self.playlistTree.setRowCount(0)
        self.gridLayout.addWidget(self.playlistTree, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 24))
        self.menuBar.setObjectName("menuBar")
        self.menuActions = QtGui.QMenu(self.menuBar)
        self.menuActions.setObjectName("menuActions")
        self.menuPlaylist = QtGui.QMenu(self.menuBar)
        self.menuPlaylist.setObjectName("menuPlaylist")
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuSettings = QtGui.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionEdit = QtGui.QAction(MainWindow)
        self.actionEdit.setObjectName("actionEdit")
        self.actionRescan_Collection = QtGui.QAction(MainWindow)
        self.actionRescan_Collection.setObjectName("actionRescan_Collection")
        self.actionExir = QtGui.QAction(MainWindow)
        self.actionExir.setObjectName("actionExir")
        self.actionPlay_Media = QtGui.QAction(MainWindow)
        self.actionPlay_Media.setObjectName("actionPlay_Media")
        self.menuActions.addAction(self.actionPlay_Media)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionExir)
        self.menuTools.addAction(self.actionRescan_Collection)
        self.menuSettings.addAction(self.actionEdit)
        self.menuBar.addAction(self.menuActions.menuAction())
        self.menuBar.addAction(self.menuPlaylist.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QtGui.QApplication.translate("MainWindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QtGui.QApplication.translate("MainWindow", "Current", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QtGui.QApplication.translate("MainWindow", "Lyrics", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), QtGui.QApplication.translate("MainWindow", "Wikipedia", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Context", None, QtGui.QApplication.UnicodeUTF8))
        self.clrBttn.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.collectTree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Artist/Album", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Media Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.prevBttn.setText(QtGui.QApplication.translate("MainWindow", "<<", None, QtGui.QApplication.UnicodeUTF8))
        self.playBttn.setText(QtGui.QApplication.translate("MainWindow", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.stopBttn.setText(QtGui.QApplication.translate("MainWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.nxtBttn.setText(QtGui.QApplication.translate("MainWindow", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.volLbl.setText(QtGui.QApplication.translate("MainWindow", "0%", None, QtGui.QApplication.UnicodeUTF8))
        self.progLbl.setText(QtGui.QApplication.translate("MainWindow", "00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlaylist.setTitle(QtGui.QApplication.translate("MainWindow", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRescan_Collection.setText(QtGui.QApplication.translate("MainWindow", "Rescan Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExir.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Media.setText(QtGui.QApplication.translate("MainWindow", "Play Media", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jon/Documents/Projects/amaroq/ui/amaroq.ui'
#
# Created: Thu Sep 17 11:12:53 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 469)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/drawing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setMargin(2)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(250, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget_2.setUsesScrollButtons(True)
        self.tabWidget_2.setDocumentMode(False)
        self.tabWidget_2.setTabsClosable(False)
        self.tabWidget_2.setMovable(False)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_12 = QtGui.QGridLayout(self.tab_6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.groupBox = QtGui.QGroupBox(self.tab_6)
        self.groupBox.setStyleSheet("""text-decoration: underline;
font: 75 10pt \"DejaVu Sans\";
""")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_8.setMargin(2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(128, 128))
        self.label_3.setMaximumSize(QtCore.QSize(128, 128))
        self.label_3.setPixmap(QtGui.QPixmap(":/Icons/music.png"))
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_2.setStyleSheet("""text-decoration: underline;
font: 75 10pt \"DejaVu Sans\";
""")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_9.setMargin(2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_9.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_3.setStyleSheet("""text-decoration: underline;
font: 75 10pt \"DejaVu Sans\";
""")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_10 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_10.setMargin(2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_10.addWidget(self.label_4, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_4.setStyleSheet("""text-decoration: underline;
font: 75 10pt \"DejaVu Sans\";
""")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_11 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_11.setMargin(2)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_11.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.groupBox_4, 3, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_8 = QtGui.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_8)
        self.gridLayout_5.setMargin(2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lyrcBrowser = QtGui.QTextBrowser(self.tab_8)
        self.lyrcBrowser.setFrameShape(QtGui.QFrame.Panel)
        self.lyrcBrowser.setFrameShadow(QtGui.QFrame.Sunken)
        self.lyrcBrowser.setObjectName("lyrcBrowser")
        self.gridLayout_5.addWidget(self.lyrcBrowser, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_9 = QtGui.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_9)
        self.gridLayout_4.setMargin(2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.wikiView = QtWebKit.QWebView(self.tab_9)
        self.wikiView.setUrl(QtCore.QUrl("about:blank"))
        self.wikiView.setObjectName("wikiView")
        self.gridLayout_4.addWidget(self.wikiView, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_9, "")
        self.gridLayout_2.addWidget(self.tabWidget_2, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setMargin(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clrBttn = QtGui.QToolButton(self.tab_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/edit-clear-locationbar-ltr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clrBttn.setIcon(icon1)
        self.clrBttn.setIconSize(QtCore.QSize(24, 24))
        self.clrBttn.setAutoRaise(True)
        self.clrBttn.setObjectName("clrBttn")
        self.horizontalLayout.addWidget(self.clrBttn)
        self.srchEdt = QtGui.QLineEdit(self.tab_2)
        self.srchEdt.setObjectName("srchEdt")
        self.horizontalLayout.addWidget(self.srchEdt)
        self.toolButton_4 = QtGui.QToolButton(self.tab_2)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout.addWidget(self.toolButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.collectTree = QtGui.QTreeWidget(self.tab_2)
        self.collectTree.setObjectName("collectTree")
        self.verticalLayout_2.addWidget(self.collectTree)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.comboBox = QtGui.QComboBox(self.tab_3)
        self.comboBox.setMaxVisibleItems(5)
        self.comboBox.setMaxCount(5)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem(QtCore.QString())
        self.horizontalLayout_5.addWidget(self.comboBox)
        self.line_2 = QtGui.QFrame(self.tab_3)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)
        self.toolButton = QtGui.QToolButton(self.tab_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/edit-rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon2)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_5.addWidget(self.toolButton)
        self.toolButton_2 = QtGui.QToolButton(self.tab_3)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon3)
        self.toolButton_2.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_5.addWidget(self.toolButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.treeWidget = QtGui.QTreeWidget(self.tab_3)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_5.addWidget(self.treeWidget)
        self.gridLayout_6.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_7 = QtGui.QGridLayout(self.tab_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton = QtGui.QPushButton(self.tab_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.tab_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_6.addWidget(self.pushButton_2)
        self.comboBox_2 = QtGui.QComboBox(self.tab_4)
        self.comboBox_2.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem(QtCore.QString())
        self.horizontalLayout_6.addWidget(self.comboBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.comboBox_3 = QtGui.QComboBox(self.tab_4)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem(QtCore.QString())
        self.verticalLayout_4.addWidget(self.comboBox_3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.toolButton_5 = QtGui.QToolButton(self.tab_4)
        self.toolButton_5.setIcon(icon1)
        self.toolButton_5.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_5.setAutoRaise(True)
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_7.addWidget(self.toolButton_5)
        self.lineEdit = QtGui.QLineEdit(self.tab_4)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_7.addWidget(self.lineEdit)
        self.toolButton_6 = QtGui.QToolButton(self.tab_4)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_7.addWidget(self.toolButton_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.treeWidget_2 = QtGui.QTreeWidget(self.tab_4)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.verticalLayout_6.addWidget(self.treeWidget_2)
        self.gridLayout_7.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.clrplyBttn = QtGui.QToolButton(self.layoutWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/edit-clear-list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clrplyBttn.setIcon(icon4)
        self.clrplyBttn.setIconSize(QtCore.QSize(24, 24))
        self.clrplyBttn.setAutoRaise(True)
        self.clrplyBttn.setObjectName("clrplyBttn")
        self.horizontalLayout_4.addWidget(self.clrplyBttn)
        self.svplyBttn = QtGui.QToolButton(self.layoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Icons/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.svplyBttn.setIcon(icon5)
        self.svplyBttn.setIconSize(QtCore.QSize(24, 24))
        self.svplyBttn.setAutoRaise(True)
        self.svplyBttn.setObjectName("svplyBttn")
        self.horizontalLayout_4.addWidget(self.svplyBttn)
        self.prvplyBttn = QtGui.QToolButton(self.layoutWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Icons/edit-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prvplyBttn.setIcon(icon6)
        self.prvplyBttn.setIconSize(QtCore.QSize(24, 24))
        self.prvplyBttn.setAutoRaise(True)
        self.prvplyBttn.setObjectName("prvplyBttn")
        self.horizontalLayout_4.addWidget(self.prvplyBttn)
        self.nxtplyBttn = QtGui.QToolButton(self.layoutWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Icons/edit-redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nxtplyBttn.setIcon(icon7)
        self.nxtplyBttn.setIconSize(QtCore.QSize(24, 24))
        self.nxtplyBttn.setAutoRaise(True)
        self.nxtplyBttn.setObjectName("nxtplyBttn")
        self.horizontalLayout_4.addWidget(self.nxtplyBttn)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.clrsrchBttn = QtGui.QToolButton(self.layoutWidget)
        self.clrsrchBttn.setIcon(icon1)
        self.clrsrchBttn.setIconSize(QtCore.QSize(24, 24))
        self.clrsrchBttn.setAutoRaise(True)
        self.clrsrchBttn.setObjectName("clrsrchBttn")
        self.horizontalLayout_4.addWidget(self.clrsrchBttn)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.srchplyEdit = QtGui.QLineEdit(self.layoutWidget)
        self.srchplyEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.srchplyEdit.setObjectName("srchplyEdit")
        self.horizontalLayout_4.addWidget(self.srchplyEdit)
        self.toolButton_3 = QtGui.QToolButton(self.layoutWidget)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_4.addWidget(self.toolButton_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.playlistTree = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlistTree.sizePolicy().hasHeightForWidth())
        self.playlistTree.setSizePolicy(sizePolicy)
        self.playlistTree.setMinimumSize(QtCore.QSize(400, 0))
        self.playlistTree.setShowGrid(False)
        self.playlistTree.setGridStyle(QtCore.Qt.DotLine)
        self.playlistTree.setObjectName("playlistTree")
        self.playlistTree.setColumnCount(0)
        self.playlistTree.setRowCount(0)
        self.playlistTree.horizontalHeader().setVisible(True)
        self.playlistTree.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.playlistTree)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prevBttn = QtGui.QToolButton(self.layoutWidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Icons/media-skip-backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevBttn.setIcon(icon8)
        self.prevBttn.setIconSize(QtCore.QSize(24, 24))
        self.prevBttn.setAutoRaise(True)
        self.prevBttn.setObjectName("prevBttn")
        self.horizontalLayout_3.addWidget(self.prevBttn)
        self.playBttn = QtGui.QToolButton(self.layoutWidget)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Icons/media-playback-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playBttn.setIcon(icon9)
        self.playBttn.setIconSize(QtCore.QSize(24, 24))
        self.playBttn.setCheckable(True)
        self.playBttn.setAutoRaise(True)
        self.playBttn.setObjectName("playBttn")
        self.horizontalLayout_3.addWidget(self.playBttn)
        self.stopBttn = QtGui.QToolButton(self.layoutWidget)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Icons/media-playback-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopBttn.setIcon(icon10)
        self.stopBttn.setIconSize(QtCore.QSize(24, 24))
        self.stopBttn.setAutoRaise(True)
        self.stopBttn.setObjectName("stopBttn")
        self.horizontalLayout_3.addWidget(self.stopBttn)
        self.nxtBttn = QtGui.QToolButton(self.layoutWidget)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/Icons/media-skip-forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nxtBttn.setIcon(icon11)
        self.nxtBttn.setIconSize(QtCore.QSize(24, 24))
        self.nxtBttn.setAutoRaise(True)
        self.nxtBttn.setObjectName("nxtBttn")
        self.horizontalLayout_3.addWidget(self.nxtBttn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.muteBttn = QtGui.QToolButton(self.layoutWidget)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/Icons/audio-volume-high.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteBttn.setIcon(icon12)
        self.muteBttn.setIconSize(QtCore.QSize(24, 24))
        self.muteBttn.setCheckable(True)
        self.muteBttn.setAutoRaise(True)
        self.muteBttn.setObjectName("muteBttn")
        self.horizontalLayout_3.addWidget(self.muteBttn)
        self.volSldr = QtGui.QSlider(self.layoutWidget)
        self.volSldr.setMaximumSize(QtCore.QSize(200, 200))
        self.volSldr.setMaximum(100)
        self.volSldr.setProperty("value", QtCore.QVariant(100))
        self.volSldr.setOrientation(QtCore.Qt.Horizontal)
        self.volSldr.setInvertedAppearance(False)
        self.volSldr.setInvertedControls(False)
        self.volSldr.setTickPosition(QtGui.QSlider.NoTicks)
        self.volSldr.setObjectName("volSldr")
        self.horizontalLayout_3.addWidget(self.volSldr)
        self.volLbl = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volLbl.sizePolicy().hasHeightForWidth())
        self.volLbl.setSizePolicy(sizePolicy)
        self.volLbl.setMinimumSize(QtCore.QSize(24, 0))
        self.volLbl.setObjectName("volLbl")
        self.horizontalLayout_3.addWidget(self.volLbl)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progSldr = QtGui.QSlider(self.layoutWidget)
        self.progSldr.setOrientation(QtCore.Qt.Horizontal)
        self.progSldr.setObjectName("progSldr")
        self.horizontalLayout_2.addWidget(self.progSldr)
        self.progLbl = QtGui.QLabel(self.layoutWidget)
        self.progLbl.setObjectName("progLbl")
        self.horizontalLayout_2.addWidget(self.progLbl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 730, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuActions = QtGui.QMenu(self.menuBar)
        self.menuActions.setObjectName("menuActions")
        self.menuPlaylist = QtGui.QMenu(self.menuBar)
        self.menuPlaylist.setObjectName("menuPlaylist")
        self.menuCurrent = QtGui.QMenu(self.menuPlaylist)
        self.menuCurrent.setObjectName("menuCurrent")
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
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPlay_Media = QtGui.QAction(MainWindow)
        self.actionPlay_Media.setObjectName("actionPlay_Media")
        self.actionMinimise_to_Tray = QtGui.QAction(MainWindow)
        self.actionMinimise_to_Tray.setCheckable(True)
        self.actionMinimise_to_Tray.setChecked(True)
        self.actionMinimise_to_Tray.setObjectName("actionMinimise_to_Tray")
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
        self.actionAbout_Amaroq = QtGui.QAction(MainWindow)
        self.actionAbout_Amaroq.setObjectName("actionAbout_Amaroq")
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuActions.addAction(self.actionPlay_Media)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionMinimise_to_Tray)
        self.menuActions.addAction(self.actionExit)
        self.menuCurrent.addAction(self.actionClear)
        self.menuCurrent.addAction(self.actionSave_2)
        self.menuCurrent.addAction(self.actionLoad)
        self.menuPlaylist.addAction(self.menuCurrent.menuAction())
        self.menuTools.addAction(self.actionUpdate_Collection)
        self.menuTools.addAction(self.actionRescan_Collection)
        self.menuSettings.addAction(self.actionEdit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Amaroq)
        self.menuBar.addAction(self.menuActions.menuAction())
        self.menuBar.addAction(self.menuPlaylist.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QObject.connect(self.clrsrchBttn, QtCore.SIGNAL("clicked()"), self.srchplyEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "amaroQ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "No Track Playing", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Fresh Podcast Episodes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Your Newest Albums", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "Favourite Albums", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QtGui.QApplication.translate("MainWindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QtGui.QApplication.translate("MainWindow", "Lyrics", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), QtGui.QApplication.translate("MainWindow", "Wikipedia", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Context", None, QtGui.QApplication.UnicodeUTF8))
        self.clrBttn.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.collectTree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Artist/Album", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "_", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("MainWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("MainWindow", "Transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("MainWindow", "No Devices Available", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_5.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_6.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Artist/Album", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Media Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.clrplyBttn.setText(QtGui.QApplication.translate("MainWindow", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.svplyBttn.setText(QtGui.QApplication.translate("MainWindow", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.prvplyBttn.setText(QtGui.QApplication.translate("MainWindow", "P", None, QtGui.QApplication.UnicodeUTF8))
        self.nxtplyBttn.setText(QtGui.QApplication.translate("MainWindow", "N", None, QtGui.QApplication.UnicodeUTF8))
        self.clrsrchBttn.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.playlistTree.setSortingEnabled(False)
        self.prevBttn.setText(QtGui.QApplication.translate("MainWindow", "<<", None, QtGui.QApplication.UnicodeUTF8))
        self.playBttn.setText(QtGui.QApplication.translate("MainWindow", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.stopBttn.setText(QtGui.QApplication.translate("MainWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.nxtBttn.setText(QtGui.QApplication.translate("MainWindow", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.muteBttn.setText(QtGui.QApplication.translate("MainWindow", "M", None, QtGui.QApplication.UnicodeUTF8))
        self.volLbl.setText(QtGui.QApplication.translate("MainWindow", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.progLbl.setText(QtGui.QApplication.translate("MainWindow", "00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlaylist.setTitle(QtGui.QApplication.translate("MainWindow", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
        self.menuCurrent.setTitle(QtGui.QApplication.translate("MainWindow", "Current", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRescan_Collection.setText(QtGui.QApplication.translate("MainWindow", "Rescan Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Media.setText(QtGui.QApplication.translate("MainWindow", "Play Media", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Media.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMinimise_to_Tray.setText(QtGui.QApplication.translate("MainWindow", "Visible", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMinimise_to_Tray.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Current.setText(QtGui.QApplication.translate("MainWindow", "Clear Current", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_2.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate_Collection.setText(QtGui.QApplication.translate("MainWindow", "Update Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Amaroq.setText(QtGui.QApplication.translate("MainWindow", "About  Amaroq", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import resource_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


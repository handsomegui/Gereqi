# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jon/Documents/Projects/Gereqi/gereqi/settings.ui'
#
# Created: Sun May 30 22:51:02 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        settings_dialog.setObjectName("settings_dialog")
        settings_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        settings_dialog.resize(480, 640)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settings_dialog.sizePolicy().hasHeightForWidth())
        settings_dialog.setSizePolicy(sizePolicy)
        settings_dialog.setMinimumSize(QtCore.QSize(480, 640))
        settings_dialog.setMaximumSize(QtCore.QSize(480, 640))
        settings_dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        settings_dialog.setWindowFilePath("")
        self.gridLayout = QtGui.QGridLayout(settings_dialog)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setMargin(1)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(settings_dialog)
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setMargin(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splash_screen = QtGui.QCheckBox(self.groupBox)
        self.splash_screen.setObjectName("splash_screen")
        self.verticalLayout.addWidget(self.splash_screen)
        self.tray_icon = QtGui.QCheckBox(self.groupBox)
        self.tray_icon.setChecked(True)
        self.tray_icon.setObjectName("tray_icon")
        self.verticalLayout.addWidget(self.tray_icon)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.tray_icon_flash = QtGui.QCheckBox(self.groupBox)
        self.tray_icon_flash.setObjectName("tray_icon_flash")
        self.horizontalLayout_2.addWidget(self.tray_icon_flash)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.player_window = QtGui.QCheckBox(self.groupBox)
        self.player_window.setObjectName("player_window")
        self.verticalLayout.addWidget(self.player_window)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.cover_size = QtGui.QSpinBox(self.groupBox)
        self.cover_size.setMinimum(24)
        self.cover_size.setMaximum(400)
        self.cover_size.setProperty("value", 200)
        self.cover_size.setObjectName("cover_size")
        self.horizontalLayout_4.addWidget(self.cover_size)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.web_browser = QtGui.QComboBox(self.groupBox)
        self.web_browser.setMinimumSize(QtCore.QSize(150, 0))
        self.web_browser.setObjectName("web_browser")
        self.horizontalLayout_3.addWidget(self.web_browser)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.other_browser = QtGui.QCheckBox(self.groupBox)
        self.other_browser.setObjectName("other_browser")
        self.horizontalLayout_5.addWidget(self.other_browser)
        self.other_browser_edit = QtGui.QLineEdit(self.groupBox)
        self.other_browser_edit.setMinimumSize(QtCore.QSize(150, 0))
        self.other_browser_edit.setObjectName("other_browser_edit")
        self.horizontalLayout_5.addWidget(self.other_browser_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setMargin(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.scores = QtGui.QRadioButton(self.groupBox_2)
        self.scores.setObjectName("scores")
        self.verticalLayout_7.addWidget(self.scores)
        self.ratings = QtGui.QRadioButton(self.groupBox_2)
        self.ratings.setChecked(True)
        self.ratings.setObjectName("ratings")
        self.verticalLayout_7.addWidget(self.ratings)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setMargin(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.remember_current = QtGui.QCheckBox(self.groupBox_3)
        self.remember_current.setObjectName("remember_current")
        self.verticalLayout_2.addWidget(self.remember_current)
        self.playlist_relative = QtGui.QCheckBox(self.groupBox_3)
        self.playlist_relative.setObjectName("playlist_relative")
        self.verticalLayout_2.addWidget(self.playlist_relative)
        self.context_browser_change = QtGui.QCheckBox(self.groupBox_3)
        self.context_browser_change.setObjectName("context_browser_change")
        self.verticalLayout_2.addWidget(self.context_browser_change)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
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
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_4 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.collection_view = QtGui.QTreeView(self.groupBox_4)
        self.collection_view.setIndentation(10)
        self.collection_view.setExpandsOnDoubleClick(True)
        self.collection_view.setObjectName("collection_view")
        self.verticalLayout_4.addWidget(self.collection_view)
        self.scan_recursively = QtGui.QCheckBox(self.groupBox_4)
        self.scan_recursively.setChecked(True)
        self.scan_recursively.setObjectName("scan_recursively")
        self.verticalLayout_4.addWidget(self.scan_recursively)
        self.watch_folders = QtGui.QCheckBox(self.groupBox_4)
        self.watch_folders.setChecked(True)
        self.watch_folders.setObjectName("watch_folders")
        self.verticalLayout_4.addWidget(self.watch_folders)
        self.verticalLayout_5.addWidget(self.groupBox_4)
        self.groupBox_5 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout = QtGui.QFormLayout(self.groupBox_5)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtGui.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.database_type = QtGui.QComboBox(self.groupBox_5)
        self.database_type.setMinimumSize(QtCore.QSize(80, 0))
        self.database_type.setMaxVisibleItems(5)
        self.database_type.setMaxCount(5)
        self.database_type.setModelColumn(0)
        self.database_type.setObjectName("database_type")
        self.database_type.addItem("")
        self.database_type.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.database_type)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QtGui.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tabWidget.addTab(self.tab_8, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(settings_dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(settings_dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(settings_dialog)
        self.tabWidget.setCurrentIndex(5)
        self.database_type.setCurrentIndex(1)
        QtCore.QObject.connect(self.other_browser, QtCore.SIGNAL("toggled(bool)"), self.other_browser_edit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(settings_dialog)

    def retranslateUi(self, settings_dialog):
        settings_dialog.setWindowTitle(QtGui.QApplication.translate("settings_dialog", "Configure - Gereqi", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("settings_dialog", "General Options", None, QtGui.QApplication.UnicodeUTF8))
        self.splash_screen.setText(QtGui.QApplication.translate("settings_dialog", "Show splash-screen on startup", None, QtGui.QApplication.UnicodeUTF8))
        self.tray_icon.setText(QtGui.QApplication.translate("settings_dialog", "Show tray icon", None, QtGui.QApplication.UnicodeUTF8))
        self.tray_icon_flash.setText(QtGui.QApplication.translate("settings_dialog", "Flash tray icon when playing", None, QtGui.QApplication.UnicodeUTF8))
        self.player_window.setText(QtGui.QApplication.translate("settings_dialog", "Show player window", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("settings_dialog", "Default size for cover previews: ", None, QtGui.QApplication.UnicodeUTF8))
        self.cover_size.setSuffix(QtGui.QApplication.translate("settings_dialog", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("settings_dialog", "External web browser: ", None, QtGui.QApplication.UnicodeUTF8))
        self.other_browser.setText(QtGui.QApplication.translate("settings_dialog", "Use another browser: ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("settings_dialog", "Components", None, QtGui.QApplication.UnicodeUTF8))
        self.scores.setText(QtGui.QApplication.translate("settings_dialog", "Use scores", None, QtGui.QApplication.UnicodeUTF8))
        self.ratings.setText(QtGui.QApplication.translate("settings_dialog", "Use ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("settings_dialog", "Playlist Window Options", None, QtGui.QApplication.UnicodeUTF8))
        self.remember_current.setText(QtGui.QApplication.translate("settings_dialog", "Remember current playlist on exit", None, QtGui.QApplication.UnicodeUTF8))
        self.playlist_relative.setText(QtGui.QApplication.translate("settings_dialog", "Manually saved playlists use relative path", None, QtGui.QApplication.UnicodeUTF8))
        self.context_browser_change.setText(QtGui.QApplication.translate("settings_dialog", "Switch to context browser on track change", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("settings_dialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("settings_dialog", "Appearance", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("settings_dialog", "Playback", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("settings_dialog", "OSD", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("settings_dialog", "Engine", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("settings_dialog", "Collection Folders", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("settings_dialog", "These folders will be scanned for media to make up your collection:", None, QtGui.QApplication.UnicodeUTF8))
        self.scan_recursively.setText(QtGui.QApplication.translate("settings_dialog", "Scan folders recursively", None, QtGui.QApplication.UnicodeUTF8))
        self.watch_folders.setText(QtGui.QApplication.translate("settings_dialog", "Watch folders for change", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("settings_dialog", "Collection Database", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("settings_dialog", "Database: ", None, QtGui.QApplication.UnicodeUTF8))
        self.database_type.setItemText(0, QtGui.QApplication.translate("settings_dialog", "MYSQL", None, QtGui.QApplication.UnicodeUTF8))
        self.database_type.setItemText(1, QtGui.QApplication.translate("settings_dialog", "SQLITE", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QtGui.QApplication.translate("settings_dialog", "Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QtGui.QApplication.translate("settings_dialog", "last.fm", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QtGui.QApplication.translate("settings_dialog", "Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("settings_dialog", "Defaults", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    settings_dialog = QtGui.QDialog()
    ui = Ui_settings_dialog()
    ui.setupUi(settings_dialog)
    settings_dialog.show()
    sys.exit(app.exec_())


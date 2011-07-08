# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jono/Gereqi/ui/setting_dialog.ui'
#
# Created: Wed Nov 25 11:39:06 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(399, 300)
        Dialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.toolBox = QtGui.QToolBox(Dialog)
        self.toolBox.setObjectName("toolBox")
        self.interface = QtGui.QWidget()
        self.interface.setGeometry(QtCore.QRect(0, 0, 381, 212))
        self.interface.setObjectName("interface")
        self.gridLayout_3 = QtGui.QGridLayout(self.interface)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.systryMsgChck = QtGui.QCheckBox(self.interface)
        self.systryMsgChck.setChecked(True)
        self.systryMsgChck.setObjectName("systryMsgChck")
        self.gridLayout_3.addWidget(self.systryMsgChck, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.toolBox.addItem(self.interface, "")
        self.library = QtGui.QWidget()
        self.library.setGeometry(QtCore.QRect(0, 0, 381, 212))
        self.library.setObjectName("library")
        self.gridLayout_2 = QtGui.QGridLayout(self.library)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.library)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.mdlbrLineEdit = QtGui.QLineEdit(self.library)
        self.mdlbrLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.mdlbrLineEdit.setObjectName("mdlbrLineEdit")
        self.gridLayout_2.addWidget(self.mdlbrLineEdit, 0, 1, 1, 1)
        self.mdlbBttn = QtGui.QToolButton(self.library)
        self.mdlbBttn.setObjectName("mdlbBttn")
        self.gridLayout_2.addWidget(self.mdlbBttn, 0, 2, 1, 1)
        self.mdlbrWtchChck = QtGui.QCheckBox(self.library)
        self.mdlbrWtchChck.setObjectName("mdlbrWtchChck")
        self.gridLayout_2.addWidget(self.mdlbrWtchChck, 1, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 124, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 1, 1, 1)
        self.toolBox.addItem(self.library, "")
        self.gridLayout.addWidget(self.toolBox, 0, 0, 1, 1)
        self.label.setBuddy(self.mdlbrLineEdit)

        self.retranslateUi(Dialog)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.systryMsgChck.setText(QtGui.QApplication.translate("Dialog", "Show Systray Messages", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.interface), QtGui.QApplication.translate("Dialog", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.mdlbBttn.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.mdlbrWtchChck.setText(QtGui.QApplication.translate("Dialog", "Watch for Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.library), QtGui.QApplication.translate("Dialog", "Media Library", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


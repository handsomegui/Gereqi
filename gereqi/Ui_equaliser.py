# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jon/Documents/Projects/Gereqi/gereqi/equaliser.ui'
#
# Created: Sun May 30 22:53:27 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(375, 188)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.presets_combo = QtGui.QComboBox(Dialog)
        self.presets_combo.setMinimumSize(QtCore.QSize(200, 0))
        self.presets_combo.setObjectName("presets_combo")
        self.horizontalLayout_2.addWidget(self.presets_combo)
        self.save_preset_bttn = QtGui.QToolButton(Dialog)
        self.save_preset_bttn.setObjectName("save_preset_bttn")
        self.horizontalLayout_2.addWidget(self.save_preset_bttn)
        self.manage_presets_bttn = QtGui.QToolButton(Dialog)
        self.manage_presets_bttn.setObjectName("manage_presets_bttn")
        self.horizontalLayout_2.addWidget(self.manage_presets_bttn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.equaliser_qroupbox = QtGui.QGroupBox(Dialog)
        self.equaliser_qroupbox.setCheckable(True)
        self.equaliser_qroupbox.setObjectName("equaliser_qroupbox")
        self.gridLayout = QtGui.QGridLayout(self.equaliser_qroupbox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.preamp = QtGui.QSlider(self.equaliser_qroupbox)
        self.preamp.setMinimum(-5)
        self.preamp.setMaximum(5)
        self.preamp.setOrientation(QtCore.Qt.Vertical)
        self.preamp.setTickPosition(QtGui.QSlider.TicksBelow)
        self.preamp.setTickInterval(1)
        self.preamp.setObjectName("preamp")
        self.verticalLayout.addWidget(self.preamp)
        self.label_12 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_12.setMinimumSize(QtCore.QSize(40, 0))
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hz30 = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz30.setMinimum(-5)
        self.hz30.setMaximum(5)
        self.hz30.setOrientation(QtCore.Qt.Vertical)
        self.hz30.setObjectName("hz30")
        self.verticalLayout_2.addWidget(self.hz30)
        self.label_2 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hz60 = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz60.setMinimum(-5)
        self.hz60.setMaximum(5)
        self.hz60.setOrientation(QtCore.Qt.Vertical)
        self.hz60.setObjectName("hz60")
        self.verticalLayout_3.addWidget(self.hz60)
        self.label_3 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.hz125 = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz125.setMinimum(-5)
        self.hz125.setMaximum(5)
        self.hz125.setOrientation(QtCore.Qt.Vertical)
        self.hz125.setObjectName("hz125")
        self.verticalLayout_4.addWidget(self.hz125)
        self.label_4 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 3, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.hz250 = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz250.setMinimum(-5)
        self.hz250.setMaximum(5)
        self.hz250.setOrientation(QtCore.Qt.Vertical)
        self.hz250.setObjectName("hz250")
        self.verticalLayout_5.addWidget(self.hz250)
        self.label_5 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 4, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.hz500 = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz500.setMinimum(-5)
        self.hz500.setMaximum(5)
        self.hz500.setOrientation(QtCore.Qt.Vertical)
        self.hz500.setObjectName("hz500")
        self.verticalLayout_6.addWidget(self.hz500)
        self.label_6 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 5, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.hz1k = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz1k.setMinimum(-5)
        self.hz1k.setMaximum(5)
        self.hz1k.setOrientation(QtCore.Qt.Vertical)
        self.hz1k.setObjectName("hz1k")
        self.verticalLayout_7.addWidget(self.hz1k)
        self.label_7 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.gridLayout.addLayout(self.verticalLayout_7, 0, 6, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.hz2k = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz2k.setMinimum(-5)
        self.hz2k.setMaximum(5)
        self.hz2k.setOrientation(QtCore.Qt.Vertical)
        self.hz2k.setObjectName("hz2k")
        self.verticalLayout_8.addWidget(self.hz2k)
        self.label_8 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.gridLayout.addLayout(self.verticalLayout_8, 0, 7, 1, 1)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.hz4k = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz4k.setMinimum(-5)
        self.hz4k.setMaximum(5)
        self.hz4k.setOrientation(QtCore.Qt.Vertical)
        self.hz4k.setObjectName("hz4k")
        self.verticalLayout_9.addWidget(self.hz4k)
        self.label_9 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.gridLayout.addLayout(self.verticalLayout_9, 0, 8, 1, 1)
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.hz8k = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz8k.setMinimum(-5)
        self.hz8k.setMaximum(5)
        self.hz8k.setOrientation(QtCore.Qt.Vertical)
        self.hz8k.setObjectName("hz8k")
        self.verticalLayout_10.addWidget(self.hz8k)
        self.label_10 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_10.addWidget(self.label_10)
        self.gridLayout.addLayout(self.verticalLayout_10, 0, 9, 1, 1)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.hz10k = QtGui.QSlider(self.equaliser_qroupbox)
        self.hz10k.setMinimum(-5)
        self.hz10k.setMaximum(5)
        self.hz10k.setOrientation(QtCore.Qt.Vertical)
        self.hz10k.setObjectName("hz10k")
        self.verticalLayout_11.addWidget(self.hz10k)
        self.label_11 = QtGui.QLabel(self.equaliser_qroupbox)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.gridLayout.addLayout(self.verticalLayout_11, 0, 10, 1, 1)
        self.gridLayout_2.addWidget(self.equaliser_qroupbox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Equaliser", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Presets:", None, QtGui.QApplication.UnicodeUTF8))
        self.save_preset_bttn.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.manage_presets_bttn.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.equaliser_qroupbox.setTitle(QtGui.QApplication.translate("Dialog", "Enable Equaliser", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Pre-amp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "30", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "60", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "125", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "250", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "500", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "1k", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "2k", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "4k", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "8k", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "10k", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


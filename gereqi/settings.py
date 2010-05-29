#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>

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


"""
This class is just for showing the settings dialog. Currently
all it does is show an empty linedit which text has to be manually
entered. An ok/cancel box then allows whatever called this dialog to
read the entered text
"""

from PyQt4.QtGui import QDialog, QLineEdit, QDialogButtonBox, \
QGridLayout, QPushButton, QFileDialog, QCheckBox, QLabel, \
QDesktopServices
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt


class Setting_Dialog(QDialog):
    def __init__(self, params):
        QDialog.__init__(self)

        self.directory = QLineEdit()
        
        self.dir_bttn = QPushButton()
        self.dir_bttn.setText("...")
        self.bttn_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                                QDialogButtonBox.Cancel)
        grid = QGridLayout()
        
        self.checker = QCheckBox("Show Messages")
        self.checker.setTristate(False)
        grid.addWidget(self.directory, 0, 0)
        grid.addWidget(self.dir_bttn, 0, 1)
        grid.addWidget(self.checker, 1, 0)
        grid.addWidget(self.bttn_box, 2, 0, 2, -1)
        self.setLayout(grid)
        
        self.setWindowTitle("Settings")
        if params["dir"] is not None:
            self.directory.setText(params["dir"])
        
        state = params["msg"]
        if state is True:
            self.checker.setCheckState(Qt.Checked)
        else:
            self.checker.setCheckState(Qt.Unchecked)
            
        self.__signals()
        
    def __signals(self):
        self.connect(self.bttn_box, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.bttn_box, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(self.dir_bttn, SIGNAL("clicked()"), self.dir_sel)
        
     
    # This is not a slot according to PyQt
    def dir_sel(self):
        dir_select = QFileDialog.getExistingDirectory(
                                None,
                                QString("Select Media Directory"),
                                QDesktopServices.storageLocation(QDesktopServices.MusicLocation),
                                QFileDialog.Options(QFileDialog.ShowDirsOnly))
                                
        if dir_select is not None:
            self.directory.setText(dir_select)
        
    def accept(self):
        if self.directory is not None:
            QDialog.accept(self)
            
    def reject(self):
        QDialog.reject(self)
        
    def finished(self):
        """
        Called externally to get the directory linedit
        """
        if self.checker.checkState() == Qt.Checked:
            state = True
        else:
            state = False        
        
        return {"dir": self.directory.text(), "msg": state}

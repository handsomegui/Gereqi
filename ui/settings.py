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
QGridLayout, QPushButton, QFileDialog
from PyQt4.QtCore import SIGNAL, SLOT


class Setting_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Setting_Dialog, self).__init__(parent)

        self.directory = QLineEdit()
        dir_bttn = QPushButton()
        dir_bttn.setText("...")
        bttn_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                   QDialogButtonBox.Cancel)
        grid = QGridLayout()
        
        grid.addWidget(self.directory, 0, 0)
        grid.addWidget(dir_bttn, 0, 1)
        grid.addWidget(bttn_box, 1, 0, 1, 2)
        self.setLayout(grid)
        
        self.connect(bttn_box, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(bttn_box, SIGNAL("rejected()"), self, SLOT("reject()"))
        #TODO: Figure out how to do custom slots, i think
        self.connect(dir_bttn, SIGNAL("clicked()"), self, SLOT("dir_sel()"))
        self.setWindowTitle("Settings")
     
    # This is not a slot according to PyQt
    def dir_sel(self):
        print("SPAM!")
        dir_select = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select Music Directory"),
            self.trUtf8("/"),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if dir_select is not None:
            self.directory.setText(dir_select)
        
    def accept(self):
        if self.directory is not None:
            QDialog.accept(self)
            
    def reject(self):
        QDialog.reject(self)
        
    def dir_val(self):
        """
        Called externally to get the directory linedit
        """
        return self.directory.text()

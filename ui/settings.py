"""
This class is just for showing the settings dialog. Currently
all it does is show an empty linedit which text has to be manually
entered. An ok/cancel box then allows whatever called this dialog to
read the entered text
"""

from PyQt4.QtGui import QDialog, QLineEdit, QDialogButtonBox, \
QGridLayout, QPushButton, QFileDialog
from PyQt4.QtCore import SIGNAL, SLOT

# Finally got round to figuring out how to do modal dialogs.
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
#        self.connect(dir_bttn, SIGNAL("clicked()"), self.dir_sel())
        self.setWindowTitle("Settings")
        
    def dir_sel(self):
        dir_select = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select Music Directory"),
            self.trUtf8("/"),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if dir_select:
            self.directory.setText(dir_select)
        
    def accept(self):
        if self.directory:
            QDialog.accept(self)
            
    def dir_val(self):
        """
        Called externally to get the directory linedit
        """
        return self.directory.text()

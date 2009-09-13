from PyQt4.QtGui import QDialog, QLineEdit, QDialogButtonBox, QGridLayout
from PyQt4.QtCore import SIGNAL, SLOT

# Finally got round to figuring out how to do modal dialogs.
class settingDlg(QDialog):
    def __init__(self, parent=None):
        super(settingDlg, self).__init__(parent)
        print "init"
        self.directory = QLineEdit()
        bttnBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                   QDialogButtonBox.Cancel)
        grid = QGridLayout()
        grid.addWidget(self.directory, 0, 0)
        grid.addWidget(bttnBox, 1, 0)
        self.setLayout(grid)
        
        self.connect(bttnBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(bttnBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.setWindowTitle("self.directory")
        
    def accept(self):
        if self.directory:
            QDialog.accept(self)
            
    def dirVal(self):
        return self.directory.text()

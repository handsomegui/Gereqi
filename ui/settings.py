from PyQt4.QtGui import QDialog, QLineEdit, QDialogButtonBox, QGridLayout, QPushButton, QFileDialog
from PyQt4.QtCore import SIGNAL, SLOT

# Finally got round to figuring out how to do modal dialogs.
class settingDlg(QDialog):
    def __init__(self, parent=None):
        super(settingDlg, self).__init__(parent)
        print "init"
        self.directory = QLineEdit()
        dirBttn = QPushButton()
        dirBttn.setText("...")
        bttnBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                   QDialogButtonBox.Cancel)
        grid = QGridLayout()
        grid.addWidget(self.directory, 0, 0)
        grid.addWidget(dirBttn, 0, 1)
        grid.addWidget(bttnBox, 1, 0, 1, 2)
        self.setLayout(grid)
        
        self.connect(bttnBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(bttnBox, SIGNAL("rejected()"), self, SLOT("reject()"))
#        self.connect(dirBttn, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.setWindowTitle("Settings")
        
    def directory(self):
            print "Spam!"
            dirselect= QFileDialog.getExistingDirectory(\
                None,
                self.trUtf8("Select Music Directory"),
                self.trUtf8("/"),
                QFileDialog.Options(QFileDialog.ShowDirsOnly))
            if dirselect:
                self.directory.setText(dirselect)
        
    def accept(self):
        if self.directory:
            QDialog.accept(self)
            
    def dirVal(self):
        return self.directory.text()

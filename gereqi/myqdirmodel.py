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

from PyQt4.QtGui import QDirModel
from PyQt4.QtCore import Qt, pyqtSignal, QModelIndex


# TODO: make readable and comment

class MyQDirModel(QDirModel):
    needsRefresh = pyqtSignal(QModelIndex)
    check_list = []
       
    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() and (index.column() == 0) and (role == Qt.CheckStateRole):
            dir_now = self.filePath(index)
            par_dir = dir_now.split("/")[:-1].join("/")
            # the item is checked only if we have stored its path
            if dir_now in self.check_list[1]:
                return Qt.Unchecked
            elif par_dir in self.check_list[1]:
                return Qt.Unchecked                 
            elif dir_now in self.check_list[0]:
                return Qt.Checked
                
            else:
                # Checks to see if a child-dir is checked
                for chk in self.check_list[0]:
                    if (chk.contains(dir_now)) and (dir_now != chk):
                        return Qt.PartiallyChecked
                        
                # Recursively go down directory from parent to 
                # see if it should be included
                checker = dir_now.split("/")
                for val in range(1, len(checker)):
                    dir_part = checker[:val+1].join("/")
                    if dir_part in self.check_list[0]:
                        return Qt.Checked 
                # Nothing found
                return Qt.Unchecked
                
        # Standard QDirModel functionality        
        else:                
            return QDirModel.data(self, index, role)        
        
    def flags(self, index):
        """
        Can not remember what this is for
        """
        if index.column() == 0: # make the first column checkable
           return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable
        else:
            return QDirModel.flags(self, index)
        
    def setData(self, index, value, role = Qt.EditRole):
        """
        Things to do on user made changes
        """
        # user trying to do something to the checkbox
        if index.isValid() and (index.column() == 0) and role == Qt.CheckStateRole:
            print self.check_list
            # store checked paths, remove unchecked paths
            if value == Qt.Checked:
                dir_now = self.filePath(index)
                # No point adding if it's root dir is already there
                checker = dir_now.split("/")
                there = False
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in self.check_list[0]:
                        there = True
                        break
                        
                try:
                    tmp_list = []
                    for exc_dir in self.check_list[1]:
                        if dir_now in exc_dir:
                            tmp_list.append(exc_dir)
                    for thing in tmp_list:
                        self.check_list[1].remove(thing)
                except ValueError:
                    # Doesn't exist yet
                    pass
                    
                if there is False:
                    self.check_list[0].append(self.filePath(index))
                self.needsRefresh.emit(index)
                return True
            
            
            # Want to exclude dir
            else:
                dir_now = self.filePath(index)
                par_dir = dir_now.split("/")[:-1].join("/")                
                tmp_list = (list(self.check_list[0]), list(self.check_list[1]))
                
                for item in tmp_list[0]:
                    # removes if we've already checked it
                    if dir_now in item:
                        self.check_list[0].remove(item)            
                 
                # Only add to unchecked if anything above is checked
                checker = dir_now.split("/")
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in self.check_list[0]:
                        self.check_list[1].append(dir_now)
                self.needsRefresh.emit(index)
                return True
         
        # Standard QDirModel functionality
        else:
            return QDirModel.setData(self, index, value, role);

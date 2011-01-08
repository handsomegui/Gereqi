
from PyQt4.QtGui import QIcon
import icons_resource

class Setup:
    def __init__(self,parent):
        self.__config_icons(parent)
        
    def __config_icons(self,parent):
        parent.clear_collect_bttn.setIcon(QIcon().fromTheme("edit-clear",
                                                                  QIcon(":/icons/edit-clear.png")))
        parent.clear_search_bttn.setIcon(QIcon().fromTheme("edit-clear"
                                                                 ,QIcon(":/icons/edit-clear.png")))
        parent.clear_trktbl_bttn.setIcon(QIcon().fromTheme("window-new",
                                                                 QIcon(":/icons/window-new.png")))
        parent.save_trktbl_bttn.setIcon(QIcon().fromTheme("document-save-as",
                                                                QIcon(":/icons/document-save-as.png")))
        parent.prev_trktbl_bttn.setIcon(QIcon().fromTheme("edit-undo",
                                                               QIcon(":/icons/edit-undo.png")))
        parent.next_trktbl_bttn.setIcon(QIcon().fromTheme("edit-redo",
                                                                QIcon(":/icons/edit-redo.png")))
        
        parent.prev_bttn.setIcon(QIcon().fromTheme("media-skip-backward",
                                                         QIcon(":/icons/media-skip-backward.png")))
        parent.play_bttn.setIcon(QIcon().fromTheme("media-playback-start",
                                                         QIcon(":/icons/media-playback-start.png")))
        parent.stop_bttn.setIcon(QIcon().fromTheme("media-playback-stop",
                                                         QIcon(":/icons/media-playback-stop.png")))
        parent.next_bttn.setIcon(QIcon().fromTheme("media-skip-forward",
                                                         QIcon(":/icons/media-skip-forward.png")))   
        
#        parent.rename_playlist_bttn.setIcon(QIcon().fromTheme("edit-rename",
#                                                                    QIcon(":/icons/document-properties")))
        parent.rename_playlist_bttn.setIcon(QIcon().fromTheme("edit-rename",
                                                                    QIcon(":/icons/document-properties.png")))
        parent.delete_playlist_bttn.setIcon(QIcon().fromTheme("edit-delete",
                                                                    QIcon(":/icons/edit-delete.png")))
        
        parent.setWindowIcon(QIcon(":/icons/app.png"))
        
        parent.mute_bttn.setIcon(QIcon().fromTheme("player-volume",
                                                         QIcon(":/icons/audio-card.png")))
        

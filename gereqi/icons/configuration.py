
from PySide.QtGui import QIcon
import icons_resource

class Setup:
    def __init__(self,parent):
        self.__config_icons(parent)
        
    def __config_icons(self,parent):
        parent.clear_collect_bttn.setIcon(QIcon().fromTheme("edit-clear",
                                                                  QIcon(":/icons/edit-clear.png")))
        parent.clear_search_bttn.setIcon(QIcon().fromTheme("edit-clear"
                                                                 ,QIcon(":/icons/edit-clear.png")))
        parent.clear_trktbl_bttn.setIcon(QIcon(":/icons/playlist-clear.png"))
        parent.save_trktbl_bttn.setIcon(QIcon(":/icons/save.png"))
        parent.prev_trktbl_bttn.setIcon(QIcon(":/icons/undo.png"))
        parent.next_trktbl_bttn.setIcon(QIcon(":/icons/redo.png"))
        
        parent.prev_bttn.setIcon(QIcon(":/icons/back.png"))
        parent.play_bttn.setIcon(QIcon(":/icons/play.png"))
        parent.stop_bttn.setIcon(QIcon(":/icons/stop.png"))
        parent.next_bttn.setIcon(QIcon(":/icons/next.png"))  
        
        parent.play_cd_actn.setIcon(QIcon(":/icons/audiocd.png"))
        parent.play_media_actn.setIcon(QIcon(":/icons/files2.png"))
        parent.prev_track_actn.setIcon(QIcon(":/icons/back.png"))
        parent.play_actn.setIcon(QIcon(":/icons/play.png"))
        parent.stop_actn.setIcon(QIcon(":/icons/stop.png"))
        parent.actionNext_Track.setIcon(QIcon(":/icons/next.png"))

        parent.rename_playlist_bttn.setIcon(QIcon().fromTheme("edit-rename",
                                                                    QIcon(":/icons/document-properties.png")))
        parent.delete_playlist_bttn.setIcon(QIcon(":/icons/remove.png"))
        
        parent.setWindowIcon(QIcon(":/icons/app.png"))
        
        parent.mute_bttn.setIcon(QIcon().fromTheme("player-volume",
                                                         QIcon(":/icons/audio-card.png")))
        

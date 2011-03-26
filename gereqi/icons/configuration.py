
from PySide.QtGui import QIcon
import icons_resource

class Setup:
    # 0 = default, 1 = legacy, 2 = system
    mode = 0;
    def __init__(self,parent):
        self.__config_icons(parent)
        
    def __config_icons(self,parent):
        icons = MyIcons()
        
        parent.clear_collect_bttn.setIcon(QIcon().fromTheme("edit-clear",
                                                                  QIcon(":/icons/edit-clear.png")))
        parent.clear_search_bttn.setIcon(QIcon().fromTheme("edit-clear"
                                                                 ,QIcon(":/icons/edit-clear.png")))
        parent.clear_trktbl_bttn.setIcon(icons.icon("clear-playlist"))
        parent.save_trktbl_bttn.setIcon(QIcon(":/icons/save.png"))
        parent.prev_trktbl_bttn.setIcon(icons.icon("undo"))
        parent.next_trktbl_bttn.setIcon(icons.icon("redo"))
        
        parent.prev_bttn.setIcon(icons.icon("back"))
        parent.play_bttn.setIcon(icons.icon("play"))
        parent.stop_bttn.setIcon(icons.icon("stop"))
        parent.next_bttn.setIcon(icons.icon("next"))  
        
        parent.play_cd_actn.setIcon(icons.icon("audiocd"))
        parent.play_media_actn.setIcon(QIcon(":/icons/files2.png"))
        parent.prev_track_actn.setIcon(QIcon(":/icons/back.png"))
        parent.play_actn.setIcon(QIcon(":/icons/play.png"))
        parent.stop_actn.setIcon(QIcon(":/icons/stop.png"))
        parent.actionNext_Track.setIcon(QIcon(":/icons/next.png"))

        parent.rename_playlist_bttn.setIcon(icons.icon("rename-playlist"))
        parent.delete_playlist_bttn.setIcon(icons.icon("delete-playlist"))
        
        parent.setWindowIcon(QIcon(":/application/app.png"))        
        parent.mute_bttn.setIcon(icons.icon("volume-max"))
        
class MyIcons:
    icons = dict()
    icons['play'] = (":/default-icons/play.png", ":/legacy-icons/play.png")
    icons['stop'] = (":/default-icons/stop.png", ":/legacy-icons/stop.png")
    icons['back'] = (":/default-icons/back.png", ":/legacy-icons/back.png")
    icons['next'] = (":/default-icons/next.png", ":/legacy-icons/next.png")
    icons['audiocd'] = (":/default-icons/audiocd.png", ":/legacy-icons/audiocd.png")
    icons["mute"] = (":/default-icons/volume-muted.png",)
    icons["volume-max"] = (":/default-icons/volume-high.png",)
    icons["undo"] = (":/default-icons/undo.png",)
    icons["redo"] = (":/default-icons/redo.png",)
    icons["clear-playlist"] = (":/default-icons/new-window.png",)
    icons["delete-playlist"] = (":/default-icons/delete.png",)
    icons["rename-playlist"] = (":/default-icons/save-as.png",)
    
    def  __init__(self, mode=0):
        self.mode = mode
        return
    
    def icon(self,name):
        return QIcon(self.icons[name][self.mode])

    
    
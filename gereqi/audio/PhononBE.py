
from PyQt4.phonon import *
import MediaTypes



class PhononBE(Phonon.MediaObject):
    def __init__(self, parent=None):
        super(PhononBE,self).__init__(parent)
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory)
        self.audio_path = Phonon.createPath(self, self.audio_output)
        
        
    def __ok_source(self, source, type):
        """
        Check source is ok to use and dynamically create a MediaSource
        """
        if type == MediaTypes.LOCALFILE:
            now = Phonon.MediaSource(source)
        elif type == MediaTypes.CD:
            d_type = Phonon.DiscType(Phonon.Cd)
            now = Phonon.MediaSource(d_type, source)
            
        return now    
        
    def load(self, track, type=MediaTypes.LOCALFILE):
        source = self.__ok_source(track, type)
        if source:
            self.enqueue(source)
        
    def is_paused(self):
        return self.state == Phonon.PausedState
     
    def is_playing(self):
        return self.state == Phonon.PlayingState
    
    def is_stopped(self):
        return self.state == Phonon.StoppedState
    
    def current_source(self):
        source = self.currentSource()
        val = {'type'   : source.type(),
               'source' : source.fileName()}
        return val

    def mute(self, val):
        self.audio_output.setMuted(val)
        
    def set_volume(self, val):
        self.audio_output.setVolume(val)
        
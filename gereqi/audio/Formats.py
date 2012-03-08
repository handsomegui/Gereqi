

"""
To find what formats are available on 
a system.
Looks in /usr/lib/ for libgst*
"""

from subprocess import call, PIPE, Popen

class Formats:
    def __init__(self):
        pass
    
    def available(self):
        # In order for certain filetypes to play the correct gstreamer
        # codecs have to be present        
        fmats = {"ogg": ["libgstvorbis.so"],
                 "flac": ["libgstflac.so"],
                 "mp3": ["libgstlame.so","libgstflump3dec.so","libmp3lame.so"],
                 "m4a": ["libfaad.so"]}
        
        # Search for the codecs using find()
        cmd = "find /usr/lib/ -name %s*"
        # Allow cuefiles by default
        avail = ["cue"]
        for key in fmats.iterkeys():
            for lib in fmats[key]:
                now = cmd % lib
                proc = Popen(now, shell=True,stdout=PIPE)
                val = proc.communicate()[0].split()
                if len(val) > 0:
                    avail.append(key)
        return avail

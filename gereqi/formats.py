

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
        fmats = {"ogg": "libgstvorbis.so",
                 "flac": "libgstflac.so",
                 "mp3": "libgstlame.so",
                 "m4a": "libfaac.so"}
        
        cmd = "find /usr/lib/ -name %s"
        avail = []
        for key in fmats.iterkeys():
            proc = Popen(cmd % fmats[key], shell=True,stdout=PIPE)
            val = proc.communicate()[0].split()
            if len(val) > 0:
                avail.append(key)
            
        return avail
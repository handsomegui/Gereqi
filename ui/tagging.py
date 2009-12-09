#!/usr/bin/env python
#TODO: Import based on gstreamer capabilities
from mutagen.flac import FLAC, FLACNoHeaderError, FLACVorbisError
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.oggvorbis import OggVorbis, OggVorbisHeaderError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3BadUnsynchData
from mutagen.asf import ASF 
from os import stat, path
import subprocess
from extraneous import Extraneous

class Fixing:
    def __init__(self):
        return
        
    def flac_bloc_fix(self, fname):
        cmd = '''metaflac --list --block-type=VORBIS_COMMENT "%s" \
            | grep "METADATA block #" \
            | cut -d"#" -f2 \
            | tr "\n" "/"  '''  % fname
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        output = proc.communicate()[0]
        cnt = [int(item) for item in output.split("/")  if item]
        
        if len(cnt) > 1:
            print("Multiple vorbis comment blocks found. Fixing:", fname)
            cnt = cnt[1:]
            cnt.reverse()
            for val in cnt:
                cmd = '''metaflac --preserve-modtime --remove --block-number=%s "%s" ''' % (val, fname)
                subprocess.call(cmd, shell=True)
        
class Manipulations:
    def treat_tracknum(self, track):
        """
        Turns the track tag into an integer
        """
        if "/" in track:
            now = track.split("/")[0]
        else:
            now = track
        return int(now)
        
    def dict_to_list(self, item):
        """
        Takes the mutagen dictionary and converts into
        a list. Catches missing values and inserts suitable
        None-values
        """
        headers = ["tracknumber", "title", "artist", "album", "date", "genre"]
        values = []
        for hdr in headers:
            try:
                if hdr == "tracknumber":
                    val = self.treat_tracknum(item[hdr][0])
                else:
                    val = item[hdr][0]
            # Used to use KeyError exception but got very odd  list-index error about 'val'
            except:
                val = None
            if not val:
                if (hdr == "tracknumber") or (hdr == "date"):
                    val = 0
                else:
                    val = "Unknown"
            values.append(val)
            
        return values
        
    def sec_to_time(self, seconds):
        """
        Converts seconds into min:sec 
        time format
        """
        minim = seconds // 60
        rem = seconds % 60
        length = "%02d:%02d" % (minim, rem)
        return length
        
    def manual_bitrate(self, fname,  item):
        f_size = stat(fname).st_size * 8
        bitrate = int(round(f_size / item.info.length / 1024))
        return bitrate
        
class Tagging:
    def __init__(self, formats):
        # Formats have to be file extensions without
        # the '.' and in lower-case
        self.a_formats = formats
        self.manip = Manipulations()
        self.extras = Extraneous()
        
    def __mp3_extract(self, fname):
        """
        mp3s require 2 instances as EasyIDE
        lacks length and bitrate tags
        """
        #FIXME: this exception implies the track 
        # can not be played which is wrong in some cases
        try:
            audio = EasyID3(fname)
            tags = self.manip.dict_to_list(audio)
        # This is likely due to having to tags at all.
        except ID3NoHeaderError, err:
            base = path.basename(fname)
            title = path.splitext(base)[0]
            tags = [0, title,  "Unknown Artist", "Unknown Album", 0, "Unknown"]
        except ID3BadUnsynchData, err:
            print "ERROR:", err, fname
            return
        try:
            other = MP3(fname)
        except HeaderNotFoundError, err: 
            print "ERROR:", err, fname
            return
        length = self.manip.sec_to_time(round(other.info.length))
        bitrate = int(round(other.info.bitrate / 1024))
        
        tags.append(length)
        tags.append(bitrate)
        return tags
        
    def __oggflac_extract(self, fname, mode):
        """
        Flacs lack bitrate tag so requires
        a simple file-size/playtime calculation.
        The values for oggs are unbelievably 
        massive
        """
        if mode == "flac":
            try:
                audio = FLAC(fname)
                bitrate = self.manip.manual_bitrate(fname, audio)
            except FLACNoHeaderError, err:
                print "ERROR:", err, fname
                return
            except  FLACVorbisError, err:
                if "> 1 Vorbis comment block found" in err:
                    fixer = Fixing()
                    fixer.flac_bloc_fix(fname)
                    audio = FLAC(fname)
                    bitrate = self.manip.manual_bitrate(fname, audio)
                else:
                    print "ERROR:", err, fname
                    return
        elif mode == "ogg":
            try:
                audio = OggVorbis(fname)
                # Damn kibibyte usage by Mutagen
                bitrate = audio.info.bitrate / 1000 
            except OggVorbisHeaderError, err:
                print "ERROR:", err, fname
                return
        length = self.manip.sec_to_time(round(audio.info.length))
        tags = self.manip.dict_to_list(audio)
        tags.append(length)
        tags.append(bitrate)
        return tags
        
        
    def extract(self, fname, mode="playlist"):
        """
        Based on the file-format extract info
        """
        if mode == "playlist":
            if not self.extras.check_source_exists(fname):
                return
            
        ext = fname.split(".")[-1].lower()
        if ext in self.a_formats:
            if ext == "flac":
                tags = self.__oggflac_extract(fname, ext)
            elif ext == "mp3":
                tags = self.__mp3_extract(fname)
            elif ext == "ogg":
                tags = self.__oggflac_extract(fname, ext)
                
            return tags

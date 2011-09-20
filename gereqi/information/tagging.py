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


#TODO: Import based on gstreamer capabilities (#gstreamer says it's near impossible)
from PyQt4.QtGui import QMessageBox

from mutagen.flac import FLAC, FLACNoHeaderError, FLACVorbisError
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.oggvorbis import OggVorbis, OggVorbisHeaderError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3BadUnsynchData
from mutagen.asf import ASF 
from mutagen.mp4 import MP4
from os import stat, path

import subprocess

class Fixing:
    def __init__(self):
        return
        
    def flac_bloc_fix(self, fname):
        """
        This is required to remove multiple block-types, comments in this case
        as this is incorrect use of this block-type. Also, mutagen can't/wont work with
        multiple comment blocks.
        """
        question = QMessageBox.question(None,
            "Flac block fixing",
            """It is likely a Flac file has multiple comment blocks. This is an incorrect use of this block-type and prevents metadata from being extracted unless fixed.

Fixing this issue is an irreversible process, would you like to continue and fix the file %s?""" % fname,
            QMessageBox.StandardButtons(\
                QMessageBox.No | \
                QMessageBox.Yes))
        
        if question == QMessageBox.No:
            return False
        
        cmd = '''metaflac --list --block-type=VORBIS_COMMENT "%s" \
            | grep "METADATA block #" \
            | cut -d"#" -f2 \
            | tr "\n" "/"  '''  % fname
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        output = proc.communicate()[0]
        cnt = [int(item) for item in output.split("/")  if item]
        
        if len(cnt) > 1:
            print("Multiple vorbis comment blocks found. Fixing: %s" % fname)
            cnt = cnt[1:]
            cnt.reverse()
            for val in cnt:
                cmd = '''metaflac --preserve-modtime --remove --block-number=%s "%s" ''' % (val, fname)
                subprocess.call(cmd, shell=True)
        
class Manipulations:
    def __treat_tracknum(self, track):
        """
        Turns the track tag into an integer
        """
        if "/" in track:
            now = track.split("/")[0]
        elif isinstance(track, tuple):
            now = track[0]
        else:
            now = track
        
        return int(now)
        
    def dict_to_list(self, item, mp4=False):
        """
        Takes the mutagen dictionary and converts into
        a list. Catches missing values and inserts suitable
        None-values
        """
        if mp4:
            headers = ["\xa9nam", "\xa9ART", "\xa9alb", "\xa9day", "\xa9gen", "trkn"]
        else:
            headers = ["title", "artist", "album", "date", "genre", "tracknumber" ]
        values = []
        for hdr in headers:
            try:
                if hdr in ["tracknumber", "trkn"]:
                    val = self.__treat_tracknum(item[hdr][0])
                else:
                    val = item[hdr][0].strip()
            # Used to use KeyError exception but got very odd  list-index error
            # about 'val'
            except:
                val = None
            if not val:
                if hdr in ["tracknumber", "date", "trkn",  "\xa9day"]:
                    val = 0
                else:
                    # FIXME: this may be unnecessarily creating titles to be "unknown"
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
            tags = ["Unknown",  "Unknown Artist", "Unknown Album", 0, "Unknown", 0]
        except ID3BadUnsynchData, err:
            print("ERROR:%s %s" % (err, fname))
            return
        try:
            other = MP3(fname)
        except HeaderNotFoundError, err: 
            print("ERROR:%s %s" % (err, fname))
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
                print("ERROR:%s %s" % (err, fname))
                return
            except  FLACVorbisError, err:
                if "> 1 Vorbis comment block found" in err:
                    fixer = Fixing()
                    if fixer.flac_bloc_fix(fname) is not False:
                        audio = FLAC(fname)
                        bitrate = self.manip.manual_bitrate(fname, audio)
                    else:
                        return
                else:
                    print("ERROR:%s %s" % (err, fname))
                    return
        elif mode == "ogg":
            try:
                audio = OggVorbis(fname)
                # Damn kibibyte usage by Mutagen
                bitrate = audio.info.bitrate / 1000 
            except OggVorbisHeaderError, err:
                print("ERROR:%s %s" % (err, fname))
                return
        length = self.manip.sec_to_time(round(audio.info.length))
        tags = self.manip.dict_to_list(audio)
        tags.append(length)
        tags.append(bitrate)
        return tags
        
    def __m4a_extract(self, fname):
        try:
            audio = MP4(fname)
        except :
            print("ERROR: %s" % fname)
            return
        tags = self.manip.dict_to_list(audio, True)
        bitrate = audio.info.bitrate / 1000
        length = self.manip.sec_to_time(round(audio.info.length))
        tags.append(length)
        tags.append(bitrate)
        return tags
        
    def extract(self, fname):
        """
        Based on the file-format extract info
        """
        ext = fname.split(".")[-1].lower()
        if ext in self.a_formats:
            if ext == "flac":
                tags = self.__oggflac_extract(fname, ext)
            elif ext == "mp3":
                tags = self.__mp3_extract(fname)
            elif ext == "ogg":
                tags = self.__oggflac_extract(fname, ext)
            elif ext == "m4a":
                tags = self.__m4a_extract(fname)
            
            if tags:
                # 'unknown' is the output from mutagen
                # also to do the conversion here last for other formats
                if tags[0].lower() == "unknown":
                    base = path.basename(fname)
                    tags[0]= path.splitext(base)[0]
                    
                year = tags[3]                
                if isinstance(year, str):
                    if "-" in year:
                        year = year.split("-")
                        year.sort()
                        year = int(year[0])
                tags[3] = year
                
                final = ["%s" % tag for tag in tags]
                return final

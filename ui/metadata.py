import tagpy

class metaData:
   
    def extract(self, fileName):
        """
        Gets the file's metadata and outputs to
        whatever needs it. tagpy doesn't return 
        safe 'empty' values so i'ev had to bodge 
        it a little with a load of try and excepts
        """
        
        tags = tagpy.FileRef(str(fileName))
        
        try:track = tags.tag().track
        except:track = 0
        
        try:
            title = tags.tag().title
            title = title.replace('''"''',"") 
            if not title:
                title = fileName.split("/")[-1]
                title = title.split(".")[0]
        except:
            title = fileName.split("/")[-1]
            title = title.split(".")[0]
        
        try:
            artist = tags.tag().artist
            artist = artist.replace('''"''',"")
        except:
            artist = ""
            
        try:
            album = tags.tag().album
            album = album.replace('''"''',"")
        except:
            album = ""

        try: 
            genre = tags.tag().genre
            genre = genre.replace('''"''',"")
        except:
            genre = ""
        
        try: year = tags.tag().year
        except: year = 0
        
        try:
            bitrate = tags.audioProperties().bitrate
        except:
            bitrate = 0
            
        try:
            seconds = tags.audioProperties().length
            min = seconds // 60
            rem = (seconds % 60) 

            length = "%02d:%02d" % (min, rem)
        except:
            length = "00:00"
        
        return [track, title, artist, album, year, genre, length, bitrate]
        
        
    def writeMeta(self, fileName, *meta):
        """
        Here, using editing tools in the main ui, the file's metadata 
        can be permanently written        
        """
        return
        


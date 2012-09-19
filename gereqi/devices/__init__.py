#!/usr/bin/env python

"""
A devicemanager which has been using the QuodLibet's similar functionality
for guidance/reference 
"""

import dbus
import os
import ConfigParser
import gpod
import sqlite3 as sqlite
import ctypes

class Udev:
    def __init__(self):
        self.__udev = ctypes.cdll.LoadLibrary("libudev.so.0")
        self.__struct = self.__udev.udev_new()
        
    def __get_attributes(self, device):
        """Pack all device attributes in a dict"""
        get_name = self.__udev.udev_list_entry_get_name
        get_value = self.__udev.udev_list_entry_get_value
        device_get_properties_list_entry = \
            self.__udev.udev_device_get_properties_list_entry
        list_entry_get_next = self.__udev.udev_list_entry_get_next

        entry = device_get_properties_list_entry(device)
        device = {}
        while entry != 0:
            name = ctypes.c_char_p(get_name(entry)).value
            value = ctypes.c_char_p(get_value(entry)).value
            device[name] = value.decode("string-escape")
            entry = list_entry_get_next(entry)
        return device

    def get_device_from_path(self, path):
        """
            Return the first device that matches the path
            i.e. /dev/sdj1
        """
        path                        = path.encode("ascii")
        udev                        = self.__udev
        enumerate_scan_devices      = udev.udev_enumerate_scan_devices
        device_new_from_syspath     = udev.udev_device_new_from_syspath
        list_entry_get_name         = udev.udev_list_entry_get_name
        enumerate_get_list_entry    = udev.udev_enumerate_get_list_entry
        device_unref                = udev.udev_device_unref
        enumerate_new               = udev.udev_enumerate_new
        enumerate_unref             = udev.udev_enumerate_unref
        enumerate_add_match_property = udev.udev_enumerate_add_match_property

        enum = enumerate_new(self.__struct)
        enumerate_add_match_property(enum, "DEVNAME", path)
        enumerate_scan_devices(enum)
        entry = enumerate_get_list_entry(enum)
        if entry != 0:
            dev = device_new_from_syspath(self.__struct,
                list_entry_get_name(entry))
            device = self.__get_attributes(dev)
            device_unref(dev)
        else:
            device = {}
        enumerate_unref(enum)

        return device

class Ipod_sql:
    def __init__(self):
        self.conn = sqlite.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                CREATE TABLE ipod
                (filename TEXT, artist VARCHAR(255), album VARCHAR(255),
                title VARCHAR(255), year SMALLINT(4), genre VARCHAR(127),
                length VARCHAR(6), bitrate SMALLINT(4), number TINYINT(2) )
                    """)
        
    def build(self,tracks):
        for trk in tracks:
            query = """INSERT INTO ipod
                        VALUES (?,?,?,?,?,?,?,?,?)"""
                        
            vals = (trk.ipod_filename(),unicode(trk['artist']),
                    unicode(trk['album']),unicode(trk['title']),trk['year'],
                    trk['genre'],trk['tracklen'],trk['bitrate'],trk['track_nr'])

            self.cursor.execute(query,vals)
            
    def artists(self):
        query = "SELECT DISTINCT artist FROM ipod ORDER BY lower(artist)"
        return (art[0] for art in self.cursor.execute(query))
        
    def albums(self):
        query = "SELECT DISTINCT album FROM ipod ORDER BY lower(album)"
        return (alb[0] for alb in self.cursor.execute(query))
    
    def find_albums(self,artist):
        query = """SELECT DISTINCT album FROM ipod
                    WHERE artist=?
                    ORDER BY lower(album)
                    """
        result = self.cursor.execute(query,(artist,)).fetchall()
        if len(result) > 0:
            return (alb[0] for alb in result)
        
    def find_tracks(self,artist="*",album="*"):
        query = """SELECT title FROM ipod
                    WHERE (artist=? OR "*"=?) 
                        AND (album=? OR "*"=?)
                    ORDER BY number"""
        results = self.cursor.execute(query,(artist,artist,album,album)).fetchall()
        
        if len(results) > 0:
            return (trk[0] for trk in results)
        
    def find_location(self,artist="*",album="*",title="*"):
        # Put the 'like's in because it was being a bit screwy
        # Might be ok when dealing with it's own outputs as inputs
        query = """SELECT filename FROM ipod
                    WHERE (artist LIKE ? OR "*"=?)
                        AND (album LIKE ? OR "*"=?)
                        AND (title LIKE ? OR "*"=?)"""
        result = self.cursor.execute(query,
                    (artist,artist,album,album,title,title)).fetchall()
        if len(result) < 1:
            return
        return (res[0] for res in result)
        
        
    def all_info(self,filename):
        query = """SELECT filename,number,title,album,artist,year,genre,length,bitrate
                    FROM ipod
                    WHERE filename=?"""
        result = self.cursor.execute(query,(filename,)).fetchone()
        hdrs = ['FileName','Track', 'Title', 'Album','Artist','Year','Genre','Length',
                'Bitrate']
        
        if len(result) < 1:
            return
            
        info = {}
        for i in range(9):
            if hdrs[i] == "Length":
                t = int(result[i]) / 1000
                min = t // 60
                rem = t % 60
                info[hdrs[i]] = "%02d:%02d" % (min, rem)
                continue
            elif (hdrs[i] == "Year") or (hdrs[i] == "Bitrate"):
                info[hdrs[i]] = str(result[i])
                continue
            
            info[hdrs[i]] = result[i] and result[i] or ""
            
        return info
        

class Ipod:
    def __init__(self,mountpoint):
        self.db = gpod.Database(mountpoint)
        self.temp_db = Ipod_sql()
        self.temp_db.build(self.db.get_master())
        
    def close(self):
        self.db.close()
    
    def artists(self):
        return self.temp_db.artists()
    
    def albums(self,artist=None):
        if artist:
            return self.temp_db.find_albums(artist)
        else:
            return self.temp_db.albums()
        
    def tracks(self,artist,album):
        return self.temp_db.find_tracks(artist, album)
    
    def filename(self,artist="*",album="*",title="*"):
        return self.temp_db.find_location(artist, album, title)
            
    def metadata(self, filename):
        return self.temp_db.all_info(filename)

class Devices:
    device_list = []
    
    def __init__(self):
        self.__udev = Udev()
        self.bus = dbus.SystemBus()
        obj = self.bus.get_object("org.freedesktop.UDisks",
                                   "/org/freedesktop/UDisks")
        
        self.interface = dbus.Interface(obj,"org.freedesktop.UDisks")
        self.props = dbus.Interface(obj,dbus.PROPERTIES_IFACE)
        
        self.__gen_device_list()
        
    def __dev_interface(self, dev):
        obj = self.bus.get_object("org.freedesktop.UDisks", dev)
        return dbus.Interface(obj, "org.freedesktop.UDisks.Device")
        

    def __properties(self,device):
        obj = self.bus.get_object("org.freedesktop.UDisks", device)
        return dbus.Interface(obj, "org.freedesktop.DBus.Properties")
    
    def __property(self,device,property):
        props = self.__properties(device)
        return props.Get("org.freedesktop.DBus.Properties", property)
    
    def __mpi_dir(self):
        base_dirs = os.getenv("XDG_DATA_DIRS")
        if base_dirs:
            base_dirs = base_dirs.split(":")
        else:
            base_dirs = ("/usr/local/share/","/usr/share/")
        
        for dir in base_dirs:
            dir_test = os.path.join(dir,"media-player-info")
            if os.path.exists(dir_test):
                return dir_test
            
    def __devices(self):        
        return (dev for dev in self.interface.EnumerateDevices()
                    if self.__property(dev, "DeviceIsRemovable"))
            
    def __mpi_file(self,dev):
        m_id = self.__media_player_id(self.__blockdev(dev))
        dir = self.__mpi_dir()
        if (not dir) or (not m_id):
            # Nothing to work with
            return
        
        m_file = os.path.join(dir,"%s.mpi" % m_id) 
        if not os.path.isfile(m_file):
            return None
        
        # Reads the .mpi file which is formatted like
        # a Windows .ini file
        parser = ConfigParser.SafeConfigParser()
        if parser.read(m_file):
            return parser
    
    def __gen_device_list(self):
        # GEt devices
        # Check for media-players
        # output as dev,blkdev,id,
        for dev in self.__devices():
            blkdev = self.__blockdev(dev)

            if not self.__media_player_id(blkdev):
                
                continue
            
            # FIXME: HACK ALERT!
            path = str(dev)
            bdev = str(blkdev)
            if self.__property(dev, "DeviceIsPartitionTable"):
                if self.__property(dev, "PartitionTableCount") > 0:
                    # A hack and guess. We can't mount /dev/sdj 
                    # as it's a partition-table. Taking a punt on
                    # what is actually mountable
                    path = "%s1" % dev
                    bdev = "%s1" % blkdev
                    # Meh, a trivial check to see that the protocols
                    # are the same. Maybe do this per partition to get
                    # the correct partition?
                    if self.protocols(path) == self.protocols(dev):
                        print "WOOPWOOP"
     
            info = {}
            # Path is the obj-path as specified by udisks
            info["PATH"] = path # dbus.ObjectPath
            info["BLKDEV"] = bdev # dbus.String
            info["ID"] = self.__dev_id(path) # dbus.String
            info["PROTOCOL"] = self.protocols(dev)[0]
            
            self.device_list.append(info)    

    
    def __blockdev(self,dev):        
        return self.__property(dev, "device-file")
    
    def __media_player_id(self,dev):
        """
        Determine whether the device is
        a media-player or not
        """
        try:
            return self.__udev.get_device_from_path(dev)["ID_MEDIA_PLAYER"]
            
        except KeyError:
#            try:
#                print self.__udev.get_device_from_path(dev)["ID_USB_DRIVER"]  
#            except KeyError: 
#                return None       
            return None
    
    def mounted(self,dev):
        if self.__property(dev, 'device-is-mounted'):
            return str(self.__property(dev, "DeviceMountPaths")[0])
        else:
            return False
        
    def mount(self,dev):
        m_state = self.mounted(dev)
        if m_state:
            print "%10s : ALREADY MOUNTED" % dev
            return m_state
        dev_if = self.__dev_interface(dev)
        m_point = dev_if.FilesystemMount("auto",["noatime"])
        return m_point
    
    def unmount(self,dev):
        if not self.mounted(dev):
            return
        dev_if = self.__dev_interface(dev)
        dev_if.FilesystemUnmount([])
    
    def __dev_id(self,dev):
        try:
            return self.__property(dev, "DeviceFileById")[0]
        except:
            #Usually the cd-drive
            return dev
        
    def vendor(self,dev):
        return self.__property(dev,"DriveVendor")
        
    def model(self,dev):
        return self.__property(dev,"DriveModel")
        
    def mountpoint(self,dev):
        print dev
        
    def protocols(self,dev):
        config = self.__mpi_file(dev)
        if not config:
            return
        prots = config.get("Device", "AccessProtocol").split(";")
        if "storage" in prots:
            prots.remove("storage")
        return prots


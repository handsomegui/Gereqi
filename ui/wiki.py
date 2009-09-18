#!/usr/bin/env python
import pycurl
#import mmap

class Wiki:
    def __init__(self):
        return
        
    # This is very bad
    def fetch(self, url):
#        dataNow = mmap.mmap(-1, 13)
        dataNow = open("/tmp/amaroqwiki", "wb")
#        dataNow = "" # This has to be a file
        print url
        url = "http://www.google.com"
        data = pycurl.Curl()
        data.setopt(data.URL, url)
        data.setopt(pycurl.USERAGENT, "Firefox/3.0.10")
        data.setopt(pycurl.FOLLOWLOCATION, 1)
        data.setopt(pycurl.MAXREDIRS, 5)
        data.setopt(pycurl.CONNECTTIMEOUT, 30)
        data.setopt(pycurl.TIMEOUT, 300)
        data.setopt(pycurl.NOSIGNAL, 1)
        data.setopt(pycurl.WRITEDATA, dataNow)
        data.perform()
        
        dataNow.close()
        dataNow = open("/tmp/amaroqwiki", "rb")
        print dataNow.read()
        
        

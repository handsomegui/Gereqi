#!/usr/bin/env python
import pycurl
import StringIO

class Wiki:
    def __init__(self):
        return
        
    # This is very bad
    def fetch(self, url):
        print url
        dataNow = StringIO.StringIO()
        data = pycurl.Curl()
        data.setopt(pycurl.URL, url)
        data.setopt(pycurl.USERAGENT, "Firefox/3.0.10")
        data.setopt(pycurl.FOLLOWLOCATION, 1)
        data.setopt(pycurl.MAXREDIRS, 5)
        data.setopt(pycurl.CONNECTTIMEOUT, 30)
        data.setopt(pycurl.TIMEOUT, 300)
        data.setopt(pycurl.NOSIGNAL, 1)
        data.setopt(pycurl.WRITEFUNCTION, dataNow.write)
        data.perform()
        
        html = dataNow.getvalue()
        return self.treat(html)
        
    def treat(self, html):
        return html

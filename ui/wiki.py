#!/usr/bin/env python

import pycurl
from StringIO import StringIO
#from urllib2 import urlopen, Request, URLError
from lxml.html import fromstring, tostring

#TODO: Put the url creation/handling in here

class Wiki:
    def fetch(self, url):
        print url, type(url)
        
#403's
#        req = Request(url)
#        try:
#            html = urlopen(req)
#            html = html.read()
#        except URLError, e:
#            print e
            
        html = StringIO()
        data = pycurl.Curl()
        data.setopt(pycurl.URL, url)
        data.setopt(pycurl.USERAGENT, "Firefox/3.0.10")
        data.setopt(pycurl.FOLLOWLOCATION, 1)
        data.setopt(pycurl.MAXREDIRS, 5)
        data.setopt(pycurl.CONNECTTIMEOUT, 30)
        data.setopt(pycurl.TIMEOUT, 300)
        data.setopt(pycurl.NOSIGNAL, 1)
        data.setopt(pycurl.WRITEFUNCTION, html.write)
        data.perform()
        
        html = html.getvalue()
        content = self.treat(html)      
       
        return content
        
    # Try and see if lxml will work again after the issue was urllib all along
    def treat(self, html):
   
        # This appears to be considerably quicker than beatifulsoup
        tree = fromstring(html)        
        try:
            tree = tree.get_element_by_id("bodyContent")
            tree = tostring(tree)
        except:
            tree = "about:blank"        
        
        return tree

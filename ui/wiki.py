#!/usr/bin/env python

import pycurl
from StringIO import StringIO
#from urllib2 import urlopen, Request, URLError
from lxml.html import fromstring, tostring

# Amazon image
#<img id="prodImage" width="240" height="240" border="0" alt="Audioslave" src="http://ecx.images-amazon.com/images/I/514QWQX4eHL._SL500_AA240_.jpg" onload="if (typeof uet == 'function') { uet('af'); }"/>
#</a>
class Wiki:
    
    #TODO:finish
    def createUrl(self, artist):
        """
        As i'm not using the api some url hackery has
        to be performed. Not finished.
        """
        exc = '''!,.%%$&(){}[]'''
        url = ''.join([c for c in artist if c not in exc])
        url = url.replace(" ", "+")
        print url
        # tried "site%%3wikipedia.org" but that is a joke. Fatboy slim == David Byrne?
        url = "http://www.google.com/search?hl=en&q=wikipedia+%s+music+OR+band+OR+artist&btnI=745" % url
        return url
        
    def fetch(self, artist):
#TODO:get urllib2 to works
#403's
#        req = Request(url)
#        try:
#            html = urlopen(req)
#            html = html.read()
#        except URLError, e:
#            print e

        url = self.createUrl(artist)
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
        
    def treat(self, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        # This appears to be considerably quicker than beatifulsoup
        tree = fromstring(html)        
        try:
            tree = tree.get_element_by_id("bodyContent")
            tree = tostring(tree)
        except:
            tree = "about:blank"        
        
        return tree

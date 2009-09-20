#!/usr/bin/env python

import pycurl
from StringIO import StringIO
#from urllib2 import urlopen, Request, URLError
from lxml.html import fromstring, tostring

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
        
        # Things to remove
        #<h3 id="siteSub">From Wikipedia, the free encyclopedia</h3>
        #<div id="contentSub"/>
        #<div class="rellink relarticle mainarticle">
        #<div class="references-small references-column-width" style="-moz-column-width: 30em;">
        #<table class="metadata plainlinks mbox-small" style="border: 1px solid rgb(170, 170, 170); background-color: rgb(249, 249, 249);">
        #<table class="navbox" cellspacing="0" style="">
        #<div id="catlinks" class="catlinks">
        

class amazon:
    def createUrl(self, artist, album):
        # The url would give google's image results
        # Only thing is google must omit amazon results
        url = "http://images.google.com/images?hl=en&source=hp&q=amazon+%s+%s" % (artist, album)
        # This may be better. Have to treat it like the wiki class. The image is in <img id="prodImage" 
        url = "http://www.google.com/search?hl=en&q=amazon+%s+%s&btnI=745" % (artist, album)

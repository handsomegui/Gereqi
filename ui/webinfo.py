#!/usr/bin/env python

#FIXME: too much of the same code duplicated
from StringIO import StringIO
from urllib2 import URLError, build_opener
from lxml.html import fromstring, tostring
import socket

timeout = 10
socket.setdefaulttimeout(timeout)

class wikipedia:
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
        url = self.createUrl(artist)
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'amaroQ')]
            html = opener.open( url ).read()
        except URLError, e:
            print e
            html = "about:blank"

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
            
#            try:
#                tree2 = fromstring(tree)
#                tree2 = tree2.find_class("references") # if it can find references we split
#                tree2 = tostring(tree2)
#                print tree2                
#            except:
#                tree2 = ""
                
            tree = tree.split('''<div class="references''')[0]
#            tree = "".join(tree)
        except:
            tree = "about:blank"        
        
        return tree
        
        # Things to remove
        #<div class="references-small">
        #<h3 id="siteSub">From Wikipedia, the free encyclopedia</h3>
        #<div id="contentSub"/>
        #<div class="rellink relarticle mainarticle">
        #<div class="references-small references-column-width" style="-moz-column-width: 30em;">
        #<table class="metadata plainlinks mbox-small" style="border: 1px solid rgb(170, 170, 170); background-color: rgb(249, 249, 249);">
        #<table class="navbox" cellspacing="0" style="">
        #<div id="catlinks" class="catlinks">
        

class amazon:
    def createUrl(self, artist, album):
        # This may be better. Have to treat it like the wiki class. The image is in <img id="prodImage" 

        artist = artist.replace(" ", "+")
        album = album.replace(" ", "+")
        url = "http://www.google.com/search?hl=en&q=amazon+%s+%s&btnI=745" % (artist, album)
        return url
       
#FIXME: oh god
    def fetch(self, artist, album):
        url = self.createUrl(artist, album)
        print url
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'amaroQ')]
            html = opener.open( url ).read()
        except URLError, e:
            print e
            html = "about:blank"

        content = self.treat(html) 
        return content
        
    def treat(self, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        imgUrl = fromstring(html)        
        try:
            imgUrl = imgUrl .get_element_by_id("prodImage")
            imgUrl  = tostring(imgUrl )
            imgUrl = imgUrl .split("src=")[1].split(" ")[0]
            imgUrl = imgUrl.strip('''"''')
        except:
            tree = "about:blank"        
        
        print imgUrl 

class switch2():
    def createUrl(self, site, *params):        
        # Cleans up the string
        for n in range(len(params)):
            exc = '''!,.%%$&(){}[]'''
            params[n] = ''.join([c for c in params[n] if c not in exc])
            params[n] = params.replace(" ", "+")
            
        params = "+".join(params)
        url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745" % (site, params)
        
        return url
        
    def fetch(self, *params):
        url = self.createUrl(site, params)
        
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'amaroQ')]
            html = opener.open( url ).read()
        except URLError, e:
            print e
            html = "about:blank"

        content = self.treat(site, html)      
       
        return content

    def treat(self, site, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        if site == "amazon": 
            tag = "prodImage"
        elif site == "wikipedia":
            tag = bodyContent
            
        tree = fromstring(html)        
        try:
            tree = tree.get_element_by_id(tag)
            tree  = tostring(tree)
        except:
            tree = "about:blank"        
        
        return tree
        

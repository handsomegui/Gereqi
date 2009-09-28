#!/usr/bin/env python

from urllib2 import URLError, build_opener
from lxml.html import fromstring, tostring
import socket
from time import time

timeout = 10
socket.setdefaulttimeout(timeout)

class webInfo:
    def createUrl(self, site, *params):
        if site == "amazon":
            print "Createurl", time() - self.tStart
            site = "amazon+uk"
        
        # Cleans up the string
        exc = '''!,.%%$&(){}[]'''
        params = params[0][0] # Hack. Result of passing *params 2 times here
        things = []
        
        for item in params:
            item = ''.join([c for c in item if c not in exc])
            item = item.replace(" ", "+")
            things.append(item)
            
        things = "+".join(things)
        if site == "wikipedia":
            things = "%s+music+OR+band+OR+artist&btnI=745" % things
            
        url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745" % (site, things)        
        return url
        
        
    def fetch(self, site, *params):
        if site == "amazon":
            print "Fetch", time() - self.tStart
            
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
            print "Treat", time() - self.tStart
            # for wikipedia cover art the image is in class="image". use src="..
            # the wikipedia method is more difficult as the image is in a named class
            # which is used more than once in the page            
            tag = "prodImage" # album art
        elif site == "wikipedia":
            tag = "bodyContent"
            
        tree = fromstring(html) # loads html into lxml        
        try:
            tree = tree.get_element_by_id(tag) #the html enclosed by the tag
            tree  = tostring(tree)
        except:
            tree = "about:blank"      

        return tree
        
    def getInfo(self, thing, *params):
        """
        Where everything starts from
        """
        
        if thing == "info":
            site = "wikipedia"
            result = self.fetch(site, params)
            result = result.split('''<div class="references''')[0] # Cuts out everything from References down
            return result
            
        elif thing == "cover":    
            self.tStart = time()
            print "Start"
            site = "amazon"
            result = self.fetch(site, params)
            html = None
            
            if result != "about:blank":
                result = result .split("src=")[1].split(" ")[0]
                result = result.strip('''"''')
                opener = build_opener()
                opener.addheaders = [('User-agent', 'amaroQ')]
                html = opener.open( result ).read()
            
            print "Finished", time() - self.tStart
            return html 

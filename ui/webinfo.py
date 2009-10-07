#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import URLError, build_opener
from lxml.html import fromstring, tostring
import socket

TIMEOUT = 10
socket.setdefaulttimeout(TIMEOUT)

class Webinfo:
    def __init__(self):
        return
        
    def create_url(self, site, *params):
        # Cleans up the string
        exc = '''!,.%%$&(){}[]'''
        things = []
        
        for item in params:
            item = ''.join([c for c in item if c not in exc])
            item = item.replace(" ", "+")
            things.append(item)
            
        things = "+".join(things)
        if "wikipedia" in site:
            things = "%s+music+OR+band+OR+artist&btnI=745" % things
            
        url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745" 
        url = url % (site, things)
        return url
        
    def fetch(self, site, *params):
        """
        Using urllib2 the html is retrieved via an url
        generated via create_url.
        """
        url = self.create_url(site, *params)

        # Here we need a check to see if the loaded link is from amazon
        # Some localisations don't seem to have the entire amazon.com 
        # catalog and the google search seems to got to discogs.com thus
        # no cover returned
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'amaroQ')]
            html = opener.open( url ).read()
        except URLError, err:
            print err
            html = "about:blank"

        content = self.treat(site, html)             
        return content


    def treat(self, site, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        
        if "amazon" in site: 
            tag = "prodImage" # album art
        elif "wikipedia" in site:
            tag = "bodyContent"
            
        tree = fromstring(html) # loads html into lxml        
        try:
            tree = tree.get_element_by_id(tag) #the html enclosed by the tag
            tree  = tostring(tree)
        except:
            tree = "about:blank"      

        return tree
        
    def get_info(self, thing, locale=None, *params):
        """
        Where everything starts from
        """
        
        if thing == "info":
            #TODO: embed a stylesheet
            # Disable underlining and higlighting of links
            site = "wikipedia"
            style = '''<style type="text/css">
         A:link {text-decoration: none; color:black}
         A:visited {text-decoration: none}
         A:active {text-decoration: none}
         A:hover {text-decoration: none}
         </style>
            '''
            result = self.fetch(site, *params)
            # Cuts out everything from References down
            result = result.split('''<div class="references''')[0] 
            result = style + result
            return result
            
        elif thing == "cover":    
            site = "amazon%s" % locale
            result = self.fetch(site, *params)
            html = None
            
            # Here we need some check that if we haven't found the cover
            # we try again not using the amazon localisation
            if result != "about:blank":
                result = result .split("src=")[1].split(" ")[0]
                result = result.strip('''"''')
                opener = build_opener()
                opener.addheaders = [('User-agent', 'amaroQ')]
                html = opener.open( result ).read()
            
            return html 

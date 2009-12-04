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
        
    def __create_url(self, site, *params):
        # Cleans up the string
        things = []
        exc = '''!,.%%$&(){}[]'''
        for item in params:
            result = ''.join([c for c in item if c not in exc])
            fin = result.replace(" ", "+")
            things.append(fin)
            
        if "wikipedia" in site:
            pre_url = "%s+music+OR+band+OR+artist" % "+".join(things)
        else:
            pre_url = "+".join(things)
            
        base_url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745" 
        url = base_url % (site, pre_url)
        return url
        
    def __fetch(self, site, *params):
        """
        Using urllib2 the html is retrieved via an url
        generated via create_url.
        """
        url = self.__create_url(site, *params)
        # Here we need a check to see if the loaded link is from amazon
        try:
            opener = build_opener()
            opener.addheaders = [('User-agent', 'Gereqi')]
            html = opener.open( url ).read()
        except URLError, err:
            print err
            html = "about:blank"
        return self.__treat(site, html)

    def __treat(self, site, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        if site == "wikipedia":
            tag = "bodyContent"
        else:
            tag = "prodImage" # album art
            
        tree = fromstring(html) # loads html into lxml        
        try:
            tree = tree.get_element_by_id(tag) #the html enclosed by the tag
            tree  = tostring(tree)
        except KeyError:
            tree = None     
        return tree
        
    def get_info(self, thing, locale=None, *params):
        """
        Where everything starts from
        """
        if thing == "info":
            site = "wikipedia"
            result = self.__fetch(site, *params)
            if result:
                base_html = '''
                <html>
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
                <style type="text/css">
                a:link {text-decoration: none; color:black;font-size 11px}
                a:visited {text-decoration: none; color:black;font-size 11px}
                a:active {text-decoration: none; color:black;font-size 11px}
                a:hover {text-decoration: none; color:black;font-size 11px}
                body{font-size: 12px}
                h1 {font-size:12px}
                h2 {font-size:11px}
                h3 {font-size:11px}
                h4 {font-size:11px}
                p {font-size:11px}
                p.normal {font-size:11px}
                p.italic {font-size:11px}
                p.oblique {font-size:11px}
                </style>
                <body>
                %s
                </body>
                </html>
                '''
                # Cuts out everything from References down
                return base_html % result.split('''<div class="references''')[0]         
            
        elif thing == "cover":    
            site = "amazon%s" % locale
            result = self.__fetch(site, *params)
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

#!/usr/bin/env python
import urllib

class Wiki:
    def __init__(self):
        return
        
    def fetch(self, url):
        print url

        html = urllib.urlopen(url)
        html = html.read()
        
        print html
        
    def treat(self, html):
        return html

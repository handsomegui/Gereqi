#!/usr/bin/env python
import urllib
#from lxml import etree
from lxml.html import document_fromstring
from lxml import etree
from StringIO import StringIO

class Wiki:
    def __init__(self):
        return
        
    def fetch(self, url):
        print url
        html = urllib.urlopen(url)
        html = html.read()
        
        self.treat(html)
        
    # Oh jesus this is hard.
    def treat(self, html):
#        <div id="bodyContent">
        parser = etree.XMLParser(ns_clean=True)
        tree = etree.parse(StringIO(html), parser)
        tree = etree.tostring(tree.getroot())
        
#        print tree[0:100]
        
        tree = document_fromstring(tree)
        
        print tree.find_class("html")
        
#        events = ("start", "end")
#        context = etree.iterparse(StringIO(html), events=events, tag="html")
#        
#        for action, elem in context:
#            print "%s: %s" % (action.elem.tag)
            
#        return etree.tostring(tree.getroot())

#        start = "bodyContent"
#        start = "html"
        
#        startPos = html.find(start)
#        print startPos

        
        
        
        
        

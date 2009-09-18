#!/usr/bin/env python
import urllib
#from lxml import etree
#from lxml.html import fromstring, parse
#from lxml.html.soupparser import fromstring
#from lxml import etree
#from StringIO import StringIO
from BeautifulSoup import BeautifulSoup

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
#        parser = etree.XMLParser(ns_clean=True)
#        tree = etree.parse(StringIO(html), parser)
#        tree = etree.tostring(tree.getroot())
        
#        print tree[0:100]
        
#        tree = fromstring(html)
#        
#        print tree.get_element_by_id("bodyContent")
        
#        events = ("start", "end")
#        context = etree.iterparse(html, tag="div")
#        for action, elem in context:
#            print "%s: %s" % (action, elem.tag)
            
#        return etree.tostring(tree.getroot())

#        start = "bodyContent"
#        start = "html"
        
#        startPos = html.find(start)
#        print startPos

#        root = fromstring(html)

        tree = BeautifulSoup(html)
        
        print type(html)
        print "the" in html        
        print tree.find(text="the")
        
        
        
        

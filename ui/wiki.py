#!/usr/bin/env python
import urllib
import pycurl
#from lxml import etree
#from lxml.html import fromstring, parse
#from lxml.html.soupparser import fromstring
#from lxml import etree
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup

class Wiki:
    def __init__(self):
        return
        
    def fetch(self, url):
        print url, type(url)
#        html = urllib.urlopen(url)
#        html = html.read()
#        
        
        
        
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
#        print html[0:100]
        content = self.treat(html)
        
       
        return content
        
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
        
#        print tree.contents
#        print type(html)
#        print "the" in html

        return tree.find("div", id="bodyContent")
        
        
        
        

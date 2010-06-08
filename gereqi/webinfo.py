#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>

# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.


from urllib2 import Request, urlopen, URLError
from lxml.html import fromstring, tostring


class Webinfo:
    def __init__(self):
        return
        
    def __create_url(self, site=None, *params):
        # Cleans up the string
        things = []
        exc = '''!,.%%$&(){}[]'''
        for item in params:
            result = filter(lambda x : x not in exc, item)
            things.append(result.replace(" ", "+"))
            
        if site == "wikipedia.org":
            pre_url = "%s+music+OR+band+OR+artist" % "+".join(things)
            base_url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745"
            url = base_url % (site, pre_url)
            return url
        elif site == "albumart.org":
            base_url = "http://www.albumart.org/index.php?srchkey=%s&itempage=1&newsearch=1&searchindex=Music"
            url = base_url % "+".join(things)
            print url
            return url
        
    def __fetch(self, url):
        """
        Using urllib2 the html is retrieved via an url
        generated via create_url.
        """
        try:
            user_agent = "Googlebot/2.1 (+http://www.google.com/bot.html)"
            headers = { 'User-Agent' : user_agent }
            req = Request(url, None, headers)
            return urlopen(req, None, 10)
        except URLError, err:
            print(err)

    def __treat(self, site, html):
        """
        Goes through, hopefully, a wikipedia page looking for data
        between div tags with id 'bodyContent'
        """
        if site == "wikipedia":
            tag = "bodyContent"
        elif site == "amazon.com":
            tag = "prodImage" # album art
        else:
            return
            
        tree = fromstring(html) # loads html into lxml        
        try:
            tree = tree.get_element_by_id(tag) #the html enclosed by the tag
            tree  = tostring(tree)
        except KeyError, err:
            print(err)
            tree = None     
        return tree
        
    def __printable_wiki(self, url):
        """
        Takes the main wiki page and returns the html
        of the printable version
        """
        title = url.split("http://en.wikipedia.org/wiki/")[-1]
        url_now = "http://en.wikipedia.org/w/index.php?title=%s&printable=yes" % title
        html = self.__fetch(url_now)
        if html is not None:
            return html.read()
        
    def get_info(self, thing, *params):
        """
        Where everything starts from
        """
        if thing == "info":
            site = "wikipedia.org"
            url = self.__create_url(site, *params)
            pre_html = self.__fetch(url)
            if pre_html is not None:
                result =  self.__printable_wiki(pre_html.geturl())
                if result is not None:
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
                    splitter = '''<h2><span class="mw-headline" id="References">References</span></h2>'''
                    final = base_html % result.split(splitter)[0] 
                    return final.encode("utf-8")       
        
        elif thing == "cover":    
            site = "albumart.org"
            url = self.__create_url(site, *params)
            pre_html = self.__fetch(url)
            if pre_html is not None:
                srch = "http://www.albumart.org/images/zoom-icon.jpg"
                html = pre_html.read().split("\n")
                html = filter(lambda x: srch in x,  html)
                images = [line.partition('</a><a href="')[2].partition('"')[0] for line in html]
                if len(images) > 0:
                    img = self.__fetch(images[0])
                    if img is not None:
                        return img.read()
                    
                else:
                    return ""

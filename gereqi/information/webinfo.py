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

import styles


class Webinfo:
    def __init__(self):
        return
        
    def __create_url(self, site=None, *params):
        # Cleans up the string
        things = []
        exc = '''!,.%%$&(){}[]'''
        for item in params:
            result = filter(lambda x : x not in exc, str(item))
            things.append(result.replace(" ", "+"))
            
        if site == "wikipedia.org":
            pre_url = "%s+music+OR+band+OR+artist" % "+".join(things)
            base_url = "http://www.google.com/search?hl=en&q=%s+%s&btnI=745"
            url = base_url % (site, pre_url)
            return url
        elif site == "albumart.org":
            base_url = "http://www.albumart.org/index.php?srchkey=%s&itempage=1&newsearch=1&searchindex=Music"
            url = base_url % "+".join(things)
            return url
        
    def __fetch(self, url):
        """
        Using urllib2 the html is retrieved via an url
        generated via create_url.
        """
        url = url.encode("utf-8")
        try:
            #TODO: use an app constant
            user_agent = "Gereqi-0.5.0" 
            headers = { 'User-Agent' : user_agent }
            req = Request(url, None, headers)
            return urlopen(req, None, 10)
        except URLError, err:
            pass
#            print(err)
        
    def __printable_wiki(self, url):
        """
        Takes the main wiki page and returns the html
        of the printable version
        """
        title = url.split("http://en.wikipedia.org/wiki/")[-1]
        url_now = "http://en.wikipedia.org/w/index.php?title=%s&printable=yes" % title
        html = self.__fetch(url_now)
        if html is not None:
            splitter = '''<h2><span class="mw-headline" id="References">References</span></h2>'''
            html = html.read().partition("<!-- content -->")[2].partition(splitter)[0]
            return html
        
    def get_info(self, thing, *params):
        """
        
        """
        if thing == "info":
            site = "wikipedia.org"
            url = self.__create_url(site, *params)
            pre_html = self.__fetch(url)
            if pre_html is not None:
                result =  self.__printable_wiki(pre_html.geturl())
                if result:
                    base_html = '''
                        <html>
                        <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
                        <style type="text/css">
                        %s
                        </style>
                        <body>
                        %s
                        </body>
                        </html>
                        ''' 
                    return base_html % (styles.stylesheet, unicode(result , "utf-8"))
        
    def get_cover(self, artist, album):
        alb = str(album).partition("(")[0].partition("[")[0]
        site = "albumart.org"
        url = self.__create_url(site, artist, alb)
        pre_html = self.__fetch(url)
        if pre_html is not None:
            srch = "http://www.albumart.org/images/zoom-icon.jpg"
            try:
                html = pre_html.read().split("\n")
                html = filter(lambda x: srch in x,  html)
                images = [line.partition('</a><a href="')[2].partition('"')[0] 
                          for line in html]
                if len(images) < 0:
                    return
                img = self.__fetch(images[0])
                if not img:
                    return
                if img.info()['Content-type'] == "image/jpeg":
                    return img.read()
            except socket.timeout:
                return


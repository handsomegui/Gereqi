import urllib
import urllib2

USER_AGENT = "gereqi-0.5.0"
TIMEOUT = 10

def fetch(url):
    hdrs = {"User-Agent": USER_AGENT}
    req = urllib2.Request(url, None, hdrs)
    try:
        resp = urllib2.urlopen(req,None,TIMEOUT)
    except urllib2.URLError, err:
        return ""
    return resp.read()
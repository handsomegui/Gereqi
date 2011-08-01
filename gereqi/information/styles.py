from PyQt4.QtGui import QFont

default_family = QFont().defaultFamily()

stylesheet = '''
body {
    font-size: 12px;
    font-family: %s;
}

a {
    text-decoration: none;
    color:black;
    font-size: 11px;
}



h1,h2,h3,h4 {
    font-size:12px;
}


p {
    font-size:11px;
}

''' % default_family

body = '''
<style type="text/css">
body {
    text-align: center;
    font-family: %s;
    }
''' % default_family

infostyles = body + '''
    
img.cover {
    width: %(width)spx;
    border: 0;
    margin: 0 auto;
    text-align: center;
}
img.mini {
    width: 48px;
    height: 48px;
    border: 0;
}


ul {
    list-style-type: none;
    font-size: 0.8em;
}

h1, h2 {
    font-size: 1em;
    color: white;
    background-color: grey;
    padding: 3px;
    margin: 3px auto;
    text-align: center;
    font-weight: bold;
    }
    
h2 {
    font-size: 0.9em;
}

#albums {
    text-align: left;
    }
    
#album a {
    text-decoration: none;
    margin: 3px auto;
    text-align: center;
    color: black;
    font-weight: bold;
}
</style>
''' 
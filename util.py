from urlparse import urlsplit
from datetime import datetime
import happybase
import config

'''
nutch_2.2.1/src/java/org/apache/nutch/util/TableUtil.java
'''
def reverseUrl(urlString):
    URL = urlsplit(urlString)

    host = URL.hostname 
    port = URL.port
    protocol = URL.scheme
    path = URL.path
    query = URL.query

    file = path
    if query:
        file = "%s?%s" % (path, query)

    # split and reverse host
    parts = host.split('.')
    ret = ".".join(parts[::-1])
    
    ret = "%s:%s" % (ret, protocol)

    if port:
        ret = "%s:%s" % (ret, port)
    
    if file:
        if file.startswith('/'):
            ret = "%s%s" % (ret, file)
        else:
            ret = "%s/%s" % (ret, file)
    return ret

def byteArrayToLong(bytes):
    return int(bytes.encode('hex'), 16)

def convertUnixTime(unixtime):
    if len(str(unixtime)) == 10:
        return datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(int(unixtime)/1000).replace(
               microsecond=(int(unixtime)%1000)*1000).strftime('%Y-%m-%d %H:%M:%S')

def getTable(revurl):
    connection = happybase.Connection(config.HBASE_HOST, autoconnect=False)
    connection.open()
    table = connection.table(config.HBASE_TABLE)
    return table

def getRow(revurl, columns=['ol', 'f']):
    table = getTable(revurl)
    row = table.row(revurl, columns)
    return row

if __name__ == "__main__":
    url = "http://bar.foo.com:8983/to/index.html?a=b&c=d#1"
    print reverseUrl(url)
    print convertUnixTime("1450300625605")


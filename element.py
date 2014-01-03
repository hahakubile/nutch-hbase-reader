from twisted.web.template import Element, renderer, XMLFile
from twisted.python.filepath import FilePath
from util import byteArrayToLong, convertUnixTime

QUALIFIER_TO_NAME = {"bas":"baseUrl",
                     "st":"status",
                     "pts":"prevFetchTime",
                     "ts":"fetchTime",
                     "fi":"fetchInterval",
                     "rsf":"retriesSinceFetch",
                     "rpr":"reprUrl",
                     "typ":"contentType",
                     "prot":"protocolStatus",
                     "mod":"modifiedTime",
                     "pmod":"prevModifiedTime",
                    }

class WebPage(Element):
    loader = XMLFile(FilePath('template.xml'))

    def __init__(self, baseurl='', revurl='', row={}):
        Element.__init__(self)
        self.baseurl = baseurl
        self.revurl  = revurl
        self.row = row

    @renderer
    def widgets_search(self, request, tag):
        tag.fillSlots(baseurl=self.baseurl,
                      revurl=self.revurl)
        return tag

    @renderer
    def widgets_outlinks(self, request, tag):
        i = 0 
        for k, v in self.row.iteritems():
            if k.startswith("ol:"):
              i += 1
              yield tag.clone().fillSlots(link=k, anchor=v, idx=str(i))

    @renderer
    def widgets_fetchfields(self, request, tag):
        for k, v in QUALIFIER_TO_NAME.iteritems():
            key = "f:%s" % k
            fieldname = v
            fieldvalue = self.row.get(key)
            
            if not fieldvalue:
                fieldvalue = ''
            elif k in ['ts', 'pts', 'mod', 'pmod']:
                value_long = byteArrayToLong(fieldvalue)
                fieldvalue = convertUnixTime(value_long)
            elif k in ['fi', 'st', 'rsf']:
                fieldvalue = str(byteArrayToLong(fieldvalue))
            else:
                fieldvalue = str(fieldvalue)
            yield tag.clone().fillSlots(fieldname=fieldname, fieldvalue=fieldvalue)


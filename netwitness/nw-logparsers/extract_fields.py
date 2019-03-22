import sys, io, codecs, json, re
from os.path import basename
from xml2json import xml2json

class myOpt:
    pretty = True

def parseFile(parserXmlPath):
    # read the first line to get codec ... if its there
    encoding = 'utf-8'
    with open(parserXmlPath, "r") as f:
        line0 = f.readline()
        if line0[0:5] == '<?xml':
            idx = line0.index('encoding=')
            idxQuoteA = idx + len('encoding=')
            quoteChar = line0[idxQuoteA:idxQuoteA+1]
            idxQuoteZ = line0.index(quoteChar, idxQuoteA+1)
            encoding = line0[idxQuoteA+1:idxQuoteZ]
    #
    lines = []
    with codecs.open(parserXmlPath, "r", encoding) as g:
        for line in g:
            if line[0:5] != ['<', '?', 'x', 'm', 'l']:
                lines.append(line)
    #
    xmlStr = "".join(lines)
    jsonStr = xml2json(xmlStr, myOpt())
    jsonObj = json.loads(jsonStr)
    return jsonObj
#

def getFileMeta(jsonObj):
    group = name = device = ""
    if "@group" in jsonObj["DEVICEMESSAGES"]:
        group = jsonObj["DEVICEMESSAGES"]["@group"]
    else:
        print("@group not in :", file=sys.stderr)
        print(jsonObj, file=sys.stderr)
    if "@name" in jsonObj["DEVICEMESSAGES"]:
        name = jsonObj["DEVICEMESSAGES"]["@name"]
    else:
        print("@name not in :", file=sys.stderr)
        print(jsonObj, file=sys.stderr)
    if "@device" in jsonObj["DEVICEMESSAGES"]:
        device = jsonObj["DEVICEMESSAGES"]["@device"]
    else:
        print("@device not in :", file=sys.stderr)
        print(jsonObj, file=sys.stderr)

    return group, name, device
#

# Fields in RSA parser expression patterns are delimited by "<",">"
# with an optional colon seperating the field name from a function or mapping
def getParseFields(parserExpression):
    result = []
    F = parserExpression.split('<')
    for i in range(1, len(F), 1):
        idxZ = F[i].find('>')
        if idxZ != -1:
            token = F[i][0:idxZ]
            idxC = token.find(':')
            if idxC != -1:
                token = token[0:idxC]
                # TODO:  Collect RHS of colon to better understand functions and methodology
            if len(token) > 1 and re.match(r'^[!A-Za-z0-9_.-]+$', token):
                result.append(token)
    return result
#

def getObjectFields(obj):
    result = []
    if "messageid" in obj:
        result.add("messageid")
    if "functions" in obj:
        functions = obj["@functions"]
        flds = getParseFields(functions)
    content = obj["@content"]
    flds = getParseFields(content)
    for f in flds:
        result.append(f)
    return result
#

def getSectionFields(jsonObj, section):
    result = set([])
    if not isinstance(jsonObj["DEVICEMESSAGES"][section], list) :
        obj = jsonObj["DEVICEMESSAGES"][section]
        flds = getObjectFields(obj)
        for f in flds:
            result.add(f)
    else:
        for obj in jsonObj["DEVICEMESSAGES"][section]:
            flds = getObjectFields(obj)
            for f in flds:
                result.add(f)
    return list(result)
#

def getHeaderFields(jsonObj):
    flds = getSectionFields(jsonObj,"HEADER")
    flds.remove("!payload")
    return flds
#

def getMessageFields(jsonObj):
    flds = getSectionFields(jsonObj,"MESSAGE")
    return flds
#

if __name__ == "__main__":
    parserXmlPath = sys.argv[1]
    jsonObj = parseFile(parserXmlPath)
    group, name, device = getFileMeta(jsonObj)
    headerFields = getHeaderFields(jsonObj)
    messageFields =  getMessageFields(jsonObj)
    for f in headerFields:
        print( "\t".join([basename(sys.argv[1]), group, name, device, "hdr", f]))
    for f in messageFields:
        print( "\t".join([basename(sys.argv[1]), group, name, device, "msg", f]))
#

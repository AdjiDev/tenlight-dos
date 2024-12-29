# > Parse Url <#
from urllib.parse import urlparse

def parseurl(target):
    parsed = urlparse(target)
    d = parsed.hostname or target.split(":")[0]
    return d
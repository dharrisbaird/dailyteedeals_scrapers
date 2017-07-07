import re
import urlparse
from datetime import datetime, timedelta
from dateutil import parser
from pyrfc3339 import generate
from commonregex import CommonRegex
from furl import furl


class ParseDate(object):

    def __call__(self, values):
        return [self.parse(value) for value in values]

    def parse(self, value):
        if isinstance(value, int) or re.match(r'\d+', value):
            value = datetime.now() + timedelta(seconds=int())
        elif isinstance(value, str):
            value = parser.parse(value)
        return generate(value, accept_naive=True)


class ExtractUrls(object):

    def __call__(self, values):
        urls = CommonRegex(" ".join(values)).links
        return list(filter(None, map(self._normalize_url, urls)))

    def _normalize_url(self, url):
        try:
            if not url.startswith('http'):
                url = 'http://' + url

            f = furl(url)
            if f.host.startswith('www.'):
                f.set(host=f.host[4:])
            if f.path.__str__().endswith(','):
                f.set(path=f.path.__str__()[:-1])
            f.set(scheme='http')
            f.remove(query=True, fragment=True)
            f.path.normalize()
            return f.url.lower()
        except Exception as err:
            print("URL Normalization error: {0}".format(err))
            pass

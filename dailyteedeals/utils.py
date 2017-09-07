# -*- coding: utf-8 -*-
import re

CURRENCIES = {
    'usd': re.compile(u'\$|usd|dollar', re.IGNORECASE),
    'gbp': re.compile(u'£|gbp|pound', re.IGNORECASE),
    'eur': re.compile(u'€|euro?|\xe2\x82\xac', re.IGNORECASE)
}


class Money(dict):
    """A very naive money parser."""

    def __init__(self, collection):
        if isinstance(collection, basestring):
            collection = collection.split(' / ')
        output = [self._parse_string(x) for x in collection]
        dict.__init__(self, filter(None, output))

    def _parse_string(self, moneyStr):
        currency = self._find_currency(moneyStr)

        result = re.search(r"(\d+(?:\.\d{1,2})?)", moneyStr)
        if not result:
            return
        cents = float(result.groups()[0]) * 100
        if cents > 0:
            return currency, int(cents)

    def _find_currency(self, moneyStr):
        for currency, pattern in CURRENCIES.items():
            if pattern.search(moneyStr) is not None:
                return currency
        
        # Default to usd
        return 'usd'
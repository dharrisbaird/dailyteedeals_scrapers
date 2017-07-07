# -*- coding: utf-8 -*-
import re


class Money(dict):
    """A very naive money parser."""

    CURRENCIES = {
        'usd': [u'$', 'usd'],
        'gbp': [u'£', 'gbp'],
        'eur': [u'€', 'eur']
    }

    def __init__(self, collection):
        if isinstance(collection, basestring):
            collection = collection.split(' / ')
        output = [self._parse_string(x) for x in collection]
        dict.__init__(self, filter(None, output))

    def _parse_string(self, moneyStr):
        moneyStr = moneyStr.decode('utf-8')
        currency = next((k for k, v in self.CURRENCIES.items()
                         for match in v if match in moneyStr.lower()), 'usd')
        result = re.search(r"(\d+(?:\.\d{1,2})?)", moneyStr)
        if not result:
            return
        cents = float(result.groups()[0]) * 100
        if cents > 0:
            return currency, int(cents)

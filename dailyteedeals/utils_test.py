# -*- coding: utf-8 -*-
import pytest
from dailyteedeals.utils import Money


@pytest.mark.parametrize('test_input,expected', [
    ('10', {'usd': 1000}),
    ('$10', {'usd': 1000}),
    ('$9.99', {'usd': 999}),
    ('£10', {'gbp': 1000}),
    (['$10', '£10', '€10'], {'gbp': 1000, 'eur': 1000, 'usd': 1000}),
    ('10 gbp', {'gbp': 1000}),
    ('10GBP', {'gbp': 1000}),
    ('$10 / £8', {'gbp': 800, 'usd': 1000}),
    ('', {}),
    ('$0', {}),
    ('0', {}),
    ('.', {}),
])
def test_eval(test_input, expected):
    assert Money(test_input) == expected

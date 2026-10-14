"""Validate reviewed server Arabic batches using the actual Frappe dictionary.
Run with bench --site SITE execute vintraxo_arabic.translation_tools.validate_server_batches.run
No business records are modified.
"""
import csv
import re
from collections import Counter
from pathlib import Path

def signature(text):
    return Counter(re.findall(r'\{[^{}]*\}|%\([^)]+\)[sdif]|(?<!%)%[sdif]|</?[A-Za-z][^>]*>', text))

def run():
    import frappe
    from frappe.translate import get_all_translations, clear_cache
    root = Path(__file__).resolve().parents[1]
    expected = {}
    batches = [root/'translation_data/education_ar.csv', *sorted((root/'translation_data').glob('server_ar_20261014*.csv'))]
    for path in batches:
        with path.open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                source, arabic = row['source'], row['arabic']
                assert signature(source) == signature(arabic), f'Unsafe placeholders or HTML: {source}'
                assert re.search('[\u0600-\u06ff]', arabic), f'Arabic missing: {source}'
                assert '\ufffd' not in arabic and '\x00' not in arabic, f'Encoding error: {source}'
                assert source not in expected or expected[source] == arabic, f'Conflicting batches: {source}'
                expected[source] = arabic
    for relative in ('translations/ar.csv', 'translation_data/custom_ar.csv'):
        with (root/relative).open(encoding='utf-8-sig', newline='') as stream:
            actual = {row[0]: row[1] for row in csv.reader(stream) if len(row)>=2}
        assert all(actual.get(s)==t for s,t in expected.items()), relative
    clear_cache()
    actual = get_all_translations('ar')
    failures = [s for s,t in expected.items() if actual.get(s)!=t.strip()]
    assert not failures, failures
    return {'validated_batches':len(batches), 'validated_translations':len(expected), 'effective_mismatches':len(failures)}

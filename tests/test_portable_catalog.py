import ast
import csv
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'vintraxo_arabic'

def read_rows(path):
    with path.open(encoding='utf-8-sig',newline='') as stream:
        return list(csv.reader(stream))

def signature(text):
    return Counter(re.findall(r'\{[^{}]*\}|%\([^)]+\)[sdif]|(?<!%)%[sdif]|</?[A-Za-z][^>]*>',text))

class PortableTranslationTests(unittest.TestCase):
    def test_runtime_catalog_is_well_formed_and_unique(self):
        rows=read_rows(APP/'translations/ar.csv')
        self.assertEqual(len(rows),26608)
        self.assertTrue(all(len(r)==2 and r[0] and r[1] for r in rows))
        self.assertEqual(len(rows),len({r[0] for r in rows}))

    def test_reviewed_batches_survive_in_runtime_and_custom_source(self):
        runtime=dict(read_rows(APP/'translations/ar.csv'))
        custom={r[0]:r[1] for r in read_rows(APP/'translation_data/custom_ar.csv')[1:]}
        paths=[APP/'translation_data/education_ar.csv',*sorted((APP/'translation_data').glob('server_ar_20261014*.csv'))]
        self.assertEqual(len(paths),6)
        reviewed={}
        for path in paths:
            with path.open(encoding='utf-8-sig',newline='') as stream:
                for row in csv.DictReader(stream):
                    source,arabic=row['source'],row['arabic']
                    self.assertEqual(signature(source),signature(arabic),source)
                    self.assertRegex(arabic,r'[\u0600-\u06ff]')
                    self.assertNotIn('\ufffd',arabic)
                    self.assertEqual(runtime[source],arabic)
                    self.assertEqual(custom[source],arabic)
                    if source in reviewed:self.assertEqual(reviewed[source],arabic)
                    reviewed[source]=arabic
        self.assertEqual(len(reviewed),2898)
        self.assertEqual(runtime['Diagnostic Module'],'قسم الفحوص التشخيصية')
        self.assertEqual(runtime['Rehabilitation and Physiotherapy'],'إعادة التأهيل والعلاج الطبيعي')

    def test_python_modules_parse_on_declared_minimum_version(self):
        for path in APP.rglob('*.py'):
            ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path),feature_version=(3,10))

    def test_package_contains_no_site_or_credential_files(self):
        for path in ROOT.rglob('*'):
            if not path.is_file():continue
            self.assertNotIn(path.name,{'site_config.json','common_site_config.json','.env'})
            self.assertNotIn(path.suffix,{'.pem','.key','.sql','.sqlite'})
            if path.suffix in {'.csv','.py','.md','.toml'}:
                self.assertNotRegex(path.read_text(encoding='utf-8-sig'),r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}')

if __name__=='__main__':unittest.main()

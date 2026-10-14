# VintraXo Arabic

Standalone Frappe app containing the Arabic runtime catalog and reviewed translation batches.
Installation does not require ERPNext, Education, Healthcare, the restaurant app, developer mode,
or a copy of the original database. Translations only affect source strings used by installed apps.

Tested with Frappe 16.33.1 / ERPNext 16.34.2. The package permits Frappe 15–16, but a fresh
installation on Frappe 15 has not been verified. Use the Python version required by your Frappe release.

See [Arabic deployment instructions](DEPLOYMENT_AR.md).

## Install from this source folder (no GitHub repository needed)

Extract the source archive to a permanent directory named `vintraxo_arabic`, outside the target bench.
Run as the bench owner, replacing the paths and site name:

```sh
cd /home/frappe/frappe-bench
bench get-app --soft-link /home/frappe/releases/vintraxo_arabic --skip-assets
bench --site your-site.example install-app vintraxo_arabic
bench --site your-site.example clear-cache
bench --site your-site.example execute vintraxo_arabic.translation_tools.validate_server_batches.run
```

The soft link points at that permanent source directory: keep it in place.
Do not use this command over an existing app directory. For an existing installation, follow the update section.
Install directly from the standalone repository with:

```sh
bench get-app https://github.com/VintrXo/vintraxo_arabic.git --branch main
bench --site your-site.example install-app vintraxo_arabic
```

## Contents and validation

- `vintraxo_arabic/translations/ar.csv`: complete runtime dictionary (26,608 unique source keys).
- `translation_data/custom_ar.csv`: maintained custom source entries; not business records.
- `translation_data/education_ar.csv` and `server_ar_20261014*.csv`: six reviewed batches.
- `translation_tools/validate_server_batches.py`: CSV, placeholders, HTML and effective Frappe dictionary validation.
- `translation_tools/audit_server_coverage.py`: read-only source coverage audit, including nested workspace JSON.

No customer records, users, site configuration, credentials or database backups are included.
Data translations and every specialized string are not claimed complete. Product names and technical codes can remain English.
Other installed translation apps or database Translation records can override entries; the validator reports conflicts.

```sh
python -m unittest discover -s tests
```

Installation/update hooks invalidate translation caches only; they do not change users' language.
Choose Arabic in the user's language setting and reload the browser with Ctrl+Shift+R.

MIT license.

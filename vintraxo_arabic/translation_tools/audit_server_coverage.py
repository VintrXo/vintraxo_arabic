"""Read-only coverage audit, including nested workspace content and legacy Desk pages."""
import csv
import json
import re
from html import unescape
from pathlib import Path

LABEL_KEYS = {'label','title','shortcut_name','card_name','chart_name','number_card_name','text','subtitle','placeholder'}
UI_FOLDERS = {'workspace','workspace_sidebar','desktop_icon','desk_page','number_card','dashboard_chart'}
SKIP_FOLDERS = {'node_modules','dist','.git','__pycache__'}

def embedded_labels(value):
    result = set()
    def visit(item):
        if isinstance(item,dict):
            for key,child in item.items():
                if isinstance(child,str):
                    if key in LABEL_KEYS:
                        text = unescape(re.sub('<[^>]+>','',child)).strip() if key=='text' else child
                        if text and re.search('[A-Za-z]',text): result.add(text)
                    if key in ('content','links'):
                        try: visit(json.loads(child))
                        except (ValueError,TypeError): pass
                visit(child)
        elif isinstance(item,list):
            for child in item: visit(child)
    visit(value)
    return result

def run():
    import frappe
    from frappe.translate import get_messages_for_app,get_messages_from_file,get_all_translations,clear_cache
    clear_cache()
    translations=get_all_translations('ar')
    report=[];summary={};warnings={}
    for app in frappe.get_installed_apps():
        if app in ('vintraxo_arabic','arabic_translations'): continue
        root=Path(frappe.get_app_path(app));sources=set();navigation=set()
        try: sources.update(m[1] for m in get_messages_for_app(app) if m[1])
        except (KeyError,ImportError) as exc:
            warnings[app]=f'{type(exc).__name__}: native extraction unavailable; using source-file fallback'
            for path in root.rglob('*'):
                if path.suffix not in ('.py','.js','.vue','.html') or SKIP_FOLDERS.intersection(path.parts):continue
                if path.stat().st_size>1_000_000:continue
                try:sources.update(m[1] for m in get_messages_from_file(str(path)) if m[1])
                except (ValueError,SyntaxError):continue
            for path in root.rglob('*.json'):
                if SKIP_FOLDERS.intersection(path.parts):continue
                try:sources.update(embedded_labels(json.loads(path.read_text())))
                except ValueError:continue
        for path in root.rglob('*.json'):
            if not UI_FOLDERS.intersection(path.parts) or SKIP_FOLDERS.intersection(path.parts):continue
            try:navigation.update(embedded_labels(json.loads(path.read_text())))
            except ValueError:continue
        sources.update(navigation)
        missing=sorted(s for s in sources if re.search('[A-Za-z]',s) and not re.search('[\u0600-\u06ff]',s) and not re.search('[\u0600-\u06ff]',translations.get(s,'')))
        summary[app]={'untranslated_candidates':len(missing),'navigation_candidates':sum(s in navigation for s in missing)}
        report.extend([app,s,'navigation' if s in navigation else 'message_or_technical'] for s in missing)
    out=Path(frappe.get_app_path('vintraxo_arabic','translation_data'))
    with (out/'server_coverage_latest.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['app','source','category']);writer.writerows(report)
    (out/'server_coverage_latest.json').write_text(json.dumps({'apps':summary,'warnings':warnings},ensure_ascii=False,indent=2))
    return {'apps':len(summary),'untranslated_candidates':len(report),'warnings':warnings}

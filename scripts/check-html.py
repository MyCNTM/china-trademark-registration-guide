"""Validate generated links, source tokens and the retained search indexing policy."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

SITE = Path(__file__).resolve().parents[1] / 'site'
errors = []
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('href', 'src') or not value: continue
            parts = urlsplit(value)
            if parts.scheme or parts.netloc or not parts.path: continue
            path = unquote(parts.path)
            target = SITE / path.removeprefix('/guide/') if path.startswith('/guide/') else page.parent / path
            if path.endswith('/'): target = target / 'index.html'
            if not target.exists(): errors.append(f'{page.relative_to(SITE)} -> {value}')
for page in SITE.rglob('*.html'):
    text = page.read_text(encoding='utf-8')
    assert '{{catalogue_' not in text, f'Unexpanded catalogue token in {page}'
    Links().feed(text)
assert not errors, '\n'.join(errors)
search = (SITE / 'classification/search.html').read_text(encoding='utf-8')
assert 'content="noindex,follow"' in search
assert 'classification-search.js?v=' in search and 'search-index.json?v=' in search
assert search.index('search-query-compat.js') < search.index('assets/javascripts/bundle.')
assert 'classification/search.html' not in (SITE / 'sitemap.xml').read_text(encoding='utf-8')
print('Validated generated links, assets, search compatibility and sitemap policy')

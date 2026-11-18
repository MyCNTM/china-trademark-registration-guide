"""Fingerprint local asset links so repeat visitors receive the matching build."""
import hashlib
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode, unquote

SITE = Path(__file__).resolve().parents[1] / 'site'
cache = {}
for page in SITE.rglob('*.html'):
    def version(match):
        key, value = match.groups()
        parts = urlsplit(value)
        if parts.scheme or parts.netloc: return match.group(0)
        path = unquote(parts.path)
        target = SITE / path.removeprefix('/guide/') if path.startswith('/guide/') else page.parent / path
        if target.suffix not in ('.js', '.css', '.json', '.svg', '.webp') or not target.is_file(): return match.group(0)
        if target not in cache: cache[target] = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
        query = dict(parse_qsl(parts.query)); query['v'] = cache[target]
        return key + '="' + urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)) + '"'
    text = page.read_text(encoding='utf-8')
    page.write_text(re.sub(r'(src|href|data-index)="([^"]+)"', version, text), encoding='utf-8')
print('Fingerprinted local scripts, styles and catalogue references')

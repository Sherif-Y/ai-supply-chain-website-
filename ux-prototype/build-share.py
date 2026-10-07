# Builds the claude.ai publish copies from the prototype source files.
# claude.ai adds the doctype/html/head/body skeleton itself, so those tags are stripped.
# Usage: python3 build-share.py          → builds every version
#        python3 build-share.py v3       → builds only v3
import os
import re
import sys

VERSIONS = {
    'v1': ('index.html', 'supply-chain-ai.html'),
    'v2': ('index-v2.html', 'applied-chain-v2.html'),
    'v3': ('index-v3.html', 'applied-chain-v3.html'),
}

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, 'share'), exist_ok=True)

for name in sys.argv[1:] or VERSIONS:
    src_name, dest_name = VERSIONS[name]
    src = open(os.path.join(here, src_name)).read()
    out = re.sub(r'<!doctype html>\s*', '', src, flags=re.I)
    out = re.sub(r'<html[^>]*>\s*', '', out).replace('</html>', '')
    out = re.sub(r'<head>\s*', '', out).replace('</head>', '')
    out = re.sub(r'<body>\s*', '', out).replace('</body>', '')
    out = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', out)
    dest = os.path.join(here, 'share', dest_name)
    open(dest, 'w').write(out.strip() + '\n')
    print(f'{name}: wrote {dest} ({len(out):,} bytes)')

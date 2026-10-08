# Builds the live website (site/index.html, published by Netlify) from the V2 draft.
# Usage: python3 ux-prototype/build-site.py
# Live-only changes: real page title and description, design notes hidden,
# and (for now) hidden from search engines. Set NOINDEX = False to allow indexing.
import os
import shutil

NOINDEX = True
TITLE = 'Applied Chain'
DESCRIPTION = 'Hire an AI workforce for your supply chain: AI planners and analysts that work in your tools and prepare decisions for your team.'

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'index-v2.html')).read()

out = src.replace('<title>Applied Chain V2</title>', f'<title>{TITLE}</title>', 1)
head = f'<meta name="description" content="{DESCRIPTION}">\n'
if NOINDEX:
    head += '<meta name="robots" content="noindex, nofollow">\n'
out = out.replace('<link rel="preconnect"', head + '<link rel="preconnect"', 1)
# Design notes are for reviews only; hide them (and their toggle) on the live site.
out = out.replace('</style>', '.notes-toggle, .note { display: none !important; }\n</style>', 1)

dest = os.path.join(os.path.dirname(here), 'site', 'index.html')
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, 'w').write(out)
# Images the page uses (e.g. images/sherif.jpg) are copied next to it.
img_src = os.path.join(here, 'images')
if os.path.isdir(img_src):
    shutil.copytree(img_src, os.path.join(os.path.dirname(dest), 'images'), dirs_exist_ok=True)
print(f'wrote {dest} ({len(out):,} bytes)')

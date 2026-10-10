# Builds the live website (site/, published by Netlify) from the V2 draft.
# Usage: python3 ux-prototype/build-site.py
# Live-only changes: real page title and description, search and share tags, favicon,
# robots.txt and sitemap.xml, and design notes hidden. Set NOINDEX = True to hide the
# site from search engines again.
import datetime
import os
import shutil

NOINDEX = False
SITE = 'https://appliedchain.ai'
TITLE = 'Applied Chain'
SHARE_TITLE = 'Applied Chain · Hire AI planners that keep your supply chain moving'
DESCRIPTION = 'Hire AI planners that keep your supply chain moving: they work alongside your team, inside the tools you already use, at every planning horizon.'
SHARE_IMAGE = f'{SITE}/images/og-image.png'

here = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.join(os.path.dirname(here), 'site')
src = open(os.path.join(here, 'index-v2.html')).read()

out = src.replace('<title>Applied Chain V2</title>', f'<title>{TITLE}</title>', 1)
head = f'''<meta name="description" content="{DESCRIPTION}">
<link rel="canonical" href="{SITE}/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/">
<meta property="og:title" content="{SHARE_TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:image" content="{SHARE_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{SHARE_TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{SHARE_IMAGE}">
'''
if NOINDEX:
    head += '<meta name="robots" content="noindex, nofollow">\n'
out = out.replace('<link rel="preconnect"', head + '<link rel="preconnect"', 1)
# Design notes are for reviews only; hide them (and their toggle) on the live site.
out = out.replace('</style>', '.notes-toggle, .note { display: none !important; }\n</style>', 1)

os.makedirs(site_dir, exist_ok=True)
open(os.path.join(site_dir, 'index.html'), 'w').write(out)

# Images the page uses (photo, share image) are copied next to it.
img_src = os.path.join(here, 'images')
if os.path.isdir(img_src):
    shutil.copytree(img_src, os.path.join(site_dir, 'images'), dirs_exist_ok=True)

# Search engine files.
robots = 'User-agent: *\nDisallow: /\n' if NOINDEX else f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n'
open(os.path.join(site_dir, 'robots.txt'), 'w').write(robots)
today = datetime.date.today().isoformat()
open(os.path.join(site_dir, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{SITE}/</loc><lastmod>{today}</lastmod></url>\n'
    '</urlset>\n')

# Browser-tab icon: the green "AC" mark.
open(os.path.join(site_dir, 'favicon.svg'), 'w').write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f6b4f"/>'
    '<text x="32" y="42" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="28" fill="#fff">AC</text></svg>\n')

print(f'wrote {site_dir}/index.html ({len(out):,} bytes), robots.txt, sitemap.xml, favicon.svg')

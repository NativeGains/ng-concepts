"""Build the Integrative Medical Pain Clinic concept for GitHub Pages.

Copies the original mockup from ship.place (page, CSS, fonts, images), inserts the
IV therapy & injections section after the Treatments section, adds a nav link,
and writes the result to _site/integrative-medical-pain-clinic/.
"""
import os, re, sys, urllib.request

ORIGIN = "https://silly-stew-019w4.ship.place"
PREFIX = "/relief-k8w3pd/"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "_site", "integrative-medical-pain-clinic")

def get(path):
    req = urllib.request.Request(ORIGIN + path, headers={"User-Agent": "Mozilla/5.0 NativeGains-build"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def save(rel, data):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(data)

ASSET = re.compile(re.escape(PREFIX) + r"([^\"'()\s>]+)")

html = get(PREFIX).decode("utf-8")
assets = set(ASSET.findall(html))
css_files = [a for a in assets if a.endswith(".css")]
for c in css_files:
    css = get(PREFIX + c).decode("utf-8")
    for a in ASSET.findall(css):
        assets.add(a)
    depth = c.count("/")
    css = ASSET.sub(lambda m: "../" * depth + m.group(1), css)
    save(c, css.encode("utf-8"))
for a in sorted(assets):
    if a in css_files or a.endswith("/") or "." not in a.split("/")[-1]:
        continue
    save(a, get(PREFIX + a))
    print("asset", a)

html = ASSET.sub(lambda m: "./" + m.group(1), html)
html = html.replace('href="' + PREFIX + '"', 'href="./"')

section = open(os.path.join(HERE, "iv-menu-section.html"), encoding="utf-8").read()
m = re.search(r'<section[^>]*id="services".*?</section>', html, re.S)
if not m:
    sys.exit("services section not found")
html = html[:m.end()] + "\n" + section + html[m.end():]

def add_nav(match):
    a_open, label, a_close = match.group(1), match.group(2), match.group(3)
    new_open = a_open.replace('href="#services"', 'href="#iv-menu"')
    return a_open + label + a_close + new_open + "IV &amp; Injections" + a_close
html, n = re.subn(r'(<a[^>]*href="#services"[^>]*>)(.*?)(</a>)', add_nav, html, flags=re.S)
print("nav links added:", n)

if 'name="robots"' not in html:
    html = html.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
html = re.sub(r'<script[^>]*cloudflareinsights[^>]*></script>', "", html)

save("index.html", html.encode("utf-8"))
print("done", len(html))

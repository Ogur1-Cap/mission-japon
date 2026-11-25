"""Build the GitHub Pages site from the single-file app source.

Usage: python3 tools/build.py
Reads app/source.html and writes index.html, manifest, service worker and icons.
"""
import json, pathlib, re
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "app" / "source.html").read_text(encoding="utf-8")
version = re.search(r'const APP_VERSION = "([^"]+)"', src).group(1)

head = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#2B3A8C">
<meta name="description" content="Apprendre le japonais du voyage, 15 minutes par jour.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Mission Japon">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,-apple-system,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator && location.protocol === "https:") {
  window.addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
}
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(head + src + tail, encoding="utf-8")

manifest = {
    "name": "Mission Japon", "short_name": "Mission Japon",
    "description": "Le japonais du voyage, 15 minutes par jour.",
    "start_url": "./", "scope": "./", "display": "standalone",
    "background_color": "#EEF1F5", "theme_color": "#2B3A8C", "lang": "fr",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
(ROOT / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

sw = (ROOT / "tools" / "sw.template.js").read_text(encoding="utf-8").replace("__VERSION__", version)
(ROOT / "sw.js").write_text(sw, encoding="utf-8")

font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
def icon(size, pad, name, round_bg):
    img = Image.new("RGBA", (size, size), (238, 241, 245, 255) if not round_bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if round_bg:
        d.ellipse((0, 0, size - 1, size - 1), fill=(43, 58, 140, 255))
    else:
        d.rectangle((0, 0, size, size), fill=(43, 58, 140, 255))
    try:
        f = ImageFont.truetype(font_path, int(size * (0.62 - pad)))
        d.text((size / 2, size / 2), "旅", font=f, fill=(255, 255, 255, 255), anchor="mm")
    except OSError:
        pass
    (ROOT / "icons").mkdir(exist_ok=True)
    img.save(ROOT / "icons" / name)
if (ROOT / "tools" / "make_icons").exists() or not (ROOT / "icons" / "icon-512.png").exists():
    icon(192, 0, "icon-192.png", False)
    icon(512, 0, "icon-512.png", False)
    icon(512, 0.14, "icon-maskable-512.png", False)
    icon(180, 0, "apple-touch-icon.png", False)
print("built version", version)

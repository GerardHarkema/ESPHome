"""Rebuild materialdesignicons-webfont.ttf with openHASP's shifted BMP codepoints.

openHASP remaps each MDI glyph from its native (often >0xFFFF) codepoint down into
the 0xE000-0xFBFF private-use range so a single BMP-only LVGL font can hold every
icon (see src/font/md-icons.json in the openHASP firmware repo). The openHASP Page
Editor VS Code extension expects an icon font that uses those same shifted
codepoints for its `\\uXXXX` preview. This script adds those shifted codepoints as
extra cmap entries (pointing at the existing glyphs) so the resulting font renders
identically to what the device firmware displays.
"""
import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).parent
SRC_FONT = HERE / "materialdesignicons-webfont.ttf"
MAPPING_JSON = HERE / "md-icons.json"
OUT_FONT = HERE / "openhasp-icons.ttf"

mapping_text = MAPPING_JSON.read_text(encoding="utf-8")
pairs = re.findall(r'"[a-z0-9\-]+":\s*"0x([0-9A-Fa-f]+)=>0x([0-9A-Fa-f]+)"', mapping_text)
if not pairs:
    sys.exit("No icon mappings found in md-icons.json")

font = TTFont(str(SRC_FONT))
cmap_tables = [t for t in font["cmap"].tables if t.isUnicode()]
if not cmap_tables:
    sys.exit("No unicode cmap subtable found in source font")

added = 0
missing = 0
for orig_hex, shifted_hex in pairs:
    orig_cp = int(orig_hex, 16)
    shifted_cp = int(shifted_hex, 16)
    glyph_name = None
    for table in cmap_tables:
        if orig_cp in table.cmap:
            glyph_name = table.cmap[orig_cp]
            break
    if glyph_name is None:
        missing += 1
        continue
    for table in cmap_tables:
        table.cmap[shifted_cp] = glyph_name
    added += 1

font.save(str(OUT_FONT))
print(f"Added {added} shifted codepoints ({missing} source glyphs not found). Wrote {OUT_FONT}")

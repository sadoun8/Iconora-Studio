#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix two issues:
1. Garbled Arabic (soft-hyphen \xad) in curved text inspector
2. Curved text SVG placed at 800x800 - need to auto-scale on first placement
"""

FILE = r"c:\Users\sadoun\Iconora Studio\frontend\src\App.jsx"

with open(FILE, encoding='utf-8') as f:
    content = f.read()

fixes = 0

# ── Fix 1: Remove soft-hyphen \xad from Arabic text ──────────────────────────
import re
before = len(content)
content = content.replace('\xad', '')   # Remove ALL soft-hyphens
after = len(content)
removed = before - after
if removed:
    print(f"Fix 1: Removed {removed} soft-hyphen characters")
    fixes += 1

# ── Fix 2: Scale curved text on first placement ───────────────────────────────
# Find the "if (!foundExisting)" block and add auto-scale
OLD_PLACEMENT = """        if (!foundExisting) {
          const vCenter = fabricCanvas.getVpCenter();
          fImg.set({ left: vCenter.x, top: vCenter.y, originX: 'center', originY: 'center' });
        }"""

NEW_PLACEMENT = """        if (!foundExisting) {
          const vCenter = fabricCanvas.getVpCenter();
          // Auto-scale to fit ~60% of canvas width so it's not giant
          const targetW = fabricCanvas.width * 0.6;
          const scaleRatio = targetW / (fImg.width || 800);
          fImg.set({
            left: vCenter.x, top: vCenter.y,
            originX: 'center', originY: 'center',
            scaleX: scaleRatio, scaleY: scaleRatio,
          });
        }"""

if OLD_PLACEMENT in content:
    content = content.replace(OLD_PLACEMENT, NEW_PLACEMENT, 1)
    print("Fix 2: Added auto-scale for curved text on first placement")
    fixes += 1
else:
    print("Fix 2 WARNING: Could not find placement block, trying alternate...")
    alt_old = "fImg.set({ left: vCenter.x, top: vCenter.y, originX: 'center', originY: 'center' });"
    alt_new = """fImg.set({
            left: vCenter.x, top: vCenter.y,
            originX: 'center', originY: 'center',
            scaleX: fabricCanvas.width * 0.6 / (fImg.width || 800),
            scaleY: fabricCanvas.width * 0.6 / (fImg.width || 800),
          });"""
    if alt_old in content:
        content = content.replace(alt_old, alt_new, 1)
        print("Fix 2 (alt): Applied")
        fixes += 1
    else:
        print("Fix 2 FAILED: Neither pattern found")

with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print(f"\nTotal fixes applied: {fixes}")
print("File written successfully.")

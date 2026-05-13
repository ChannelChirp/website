#!/usr/bin/env python3
"""
Strip front matter to only: layout, date, categories, permalink, title.
Converts layout: post -> layout: default.
Handles UTF-8 BOM and preserves original key order.
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"
KEEP_KEYS = {"layout", "date", "categories", "permalink", "title"}
REPLACE_LAYOUT = True
NEW_LAYOUT = "default"

def parse_front_matter(text):
    """Extract front matter lines and content. Returns (lines, content) or None."""
    match = re.match(r'^\s*---\s*\n(.*?)\n\s*---\s*\n', text, re.DOTALL)
    if not match:
        return None
    fm_raw = match.group(1)
    content = text[match.end():]
    lines = fm_raw.splitlines()
    return lines, content

def rebuild_front_matter(lines):
    """Keep only lines with keys in KEEP_KEYS; optionally replace layout value."""
    kept = []
    for line in lines:
        for key in KEEP_KEYS:
            if re.match(rf'^{re.escape(key)}\s*:', line):
                if key == "layout" and REPLACE_LAYOUT:
                    line = re.sub(r'^(layout\s*:\s*).*$', rf'\1{NEW_LAYOUT}', line)
                kept.append(line)
                break
    return kept

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove BOM if present
    text = text.lstrip('\ufeff')

    # Create backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(text)

    result = parse_front_matter(text)
    if result is None:
        print(f"❌ No front matter: {os.path.basename(filepath)}")
        return

    fm_lines, content = result
    kept_lines = rebuild_front_matter(fm_lines)

    new_fm = "---\n" + "\n".join(kept_lines) + "\n---\n"
    new_text = new_fm + content

    if new_text != text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"✅ Cleaned: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  Already clean: {os.path.basename(filepath)}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"❌ Directory '{POSTS_DIR}' not found. Run this script from your project root.")
        return

    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    if not md_files:
        print("No .md files found in _posts.")
        return

    for filename in sorted(md_files):
        process_file(os.path.join(POSTS_DIR, filename))
    print("\n✔️  All done. Backups saved as .bak inside _posts/")

if __name__ == "__main__":
    main()
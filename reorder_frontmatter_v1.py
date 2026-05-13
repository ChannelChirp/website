#!/usr/bin/env python3
"""
Reorder Jekyll front matter keys: layout, title, date, categories, permalink.
Keeps everything else intact and creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"
DESIRED_ORDER = ["layout", "title", "date", "categories", "permalink"]

def parse_front_matter(text):
    match = re.match(r'^\s*---\s*\n(.*?)\n\s*---\s*\n', text, re.DOTALL)
    if not match:
        return None, text
    fm_raw = match.group(1)
    content = text[match.end():]
    lines = fm_raw.splitlines()
    return lines, content

def rebuild_ordered(lines, order):
    # Build a dict: key -> original line
    mapping = {}
    for line in lines:
        for key in order:
            if re.match(rf'^{re.escape(key)}\s*:', line):
                mapping[key] = line
                break
    # Return lines in desired order, skipping any missing keys
    return [mapping[k] for k in order if k in mapping]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.lstrip('\ufeff')
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(text)

    fm_lines, content = parse_front_matter(text)
    if fm_lines is None:
        print(f"⚠️  No front matter: {os.path.basename(filepath)}")
        return

    ordered = rebuild_ordered(fm_lines, DESIRED_ORDER)
    new_fm = "---\n" + "\n".join(ordered) + "\n---\n"
    new_text = new_fm + content

    if new_text != text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"✅ Reordered: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  Already ordered: {os.path.basename(filepath)}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"'{POSTS_DIR}' not found. Run from project root.")
        return
    for fname in sorted(os.listdir(POSTS_DIR)):
        if fname.endswith(".md"):
            process_file(os.path.join(POSTS_DIR, fname))
    print("Done.")

if __name__ == "__main__":
    main()
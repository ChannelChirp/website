#!/usr/bin/env python3
"""
Convert HTML entities in Jekyll front matter to Unicode characters.
- Uses only the standard library
- Modifies .md files inside _posts
- Creates .bak backups
"""

import os
import re
import html

POSTS_DIR = "_posts"

def unescape_front_matter(text):
    """Find the front matter block and unescape HTML entities inside it."""
    pattern = re.compile(r'^(---\s*\n)(.*?)(\n---\s*\n)', re.DOTALL)
    match = pattern.match(text)
    if not match:
        return text

    before = match.group(1)
    fm_content = match.group(2)
    after = match.group(3)
    rest = text[match.end():]

    unescaped = html.unescape(fm_content)
    return before + unescaped + after + rest

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    # Backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(original)

    converted = unescape_front_matter(original)

    if converted != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"✅ Unescaped: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  No changes: {os.path.basename(filepath)}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"❌ Directory '{POSTS_DIR}' not found.")
        return

    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith(".md"):
            process_file(os.path.join(POSTS_DIR, filename))
    print("\n✔️  Done. Backups inside _posts/")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Insert a blank line after Liquid tags that are immediately followed by
a single space (to properly separate the embed from subsequent text).
Example:
  {% include embed/youtube.html id="w0mf_AGLago" %} Example text
becomes:
  {% include embed/youtube.html id="w0mf_AGLago" %}

  Example text
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"

# Match a Liquid closing delimiter '%}' followed by a literal space character
PATTERN = re.compile(r'%\}( )')   # group(1) is the space

def process_content(text):
    # Replace '%} ' with '%}\n\n' (two newlines for a blank line)
    return PATTERN.sub(r'%}\n\n', text)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    original = original.lstrip('\ufeff')

    # Backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(original)

    modified = process_content(original)

    if modified != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"✅ Fixed spacing: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  No changes: {os.path.basename(filepath)}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"❌ Directory '{POSTS_DIR}' not found. Run from project root.")
        return

    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            process_file(os.path.join(POSTS_DIR, filename))
    print("\n✔️  Done. Backups saved as .bak inside _posts/")

if __name__ == "__main__":
    main()
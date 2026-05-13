#!/usr/bin/env python3
"""
Set layout: post for all .md files in _posts/
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"

def set_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(text)

    # Replace layout line (case‑insensitive, any value)
    new_text = re.sub(
        r'^(layout\s*:\s*).*$',
        r'\1post',
        text,
        flags=re.MULTILINE | re.IGNORECASE
    )

    if new_text != text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"✅ Set layout:post → {os.path.basename(filepath)}")
    else:
        print(f"⏺️  Already post: {os.path.basename(filepath)}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"❌ '{POSTS_DIR}' not found. Run from project root.")
        return

    for fname in sorted(os.listdir(POSTS_DIR)):
        if fname.endswith('.md'):
            set_layout(os.path.join(POSTS_DIR, fname))
    print("\n✔️  Done. Backups in _posts/")

if __name__ == "__main__":
    main()
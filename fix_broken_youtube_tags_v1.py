#!/usr/bin/env python3
"""
Repair broken Liquid YouTube includes that were split by a Markdown escape.
Example: {% include embed/youtube.html id="e9aXe9" %}\_0XMY
      -> {% include embed/youtube.html id="e9aXe9_0XMY" %}
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"

# Pattern: a Liquid include with id="PART", then an escaped fragment like \_rest
BROKEN_TAG_RE = re.compile(
    r'(\{%\s*include\s+embed/youtube\.html\s+id="(?P<id>[^"]*)"\s*%\})'
    r'(?P<rest>(?:\\[^\s])+)'   # one or more backslash-escaped chars
)

def fix_broken(text):
    """Merge broken Liquid tags with their escaped suffix."""
    def merge(m):
        tag_start = m.group(1)  # {% include ... id="e9aXe9" %}
        escaped = m.group('rest')   # \_0XMY
        # Remove all backslashes from escaped part to recover original ID segment
        clean_suffix = escaped.replace('\\', '')
        # Insert the suffix into the id value, just before the closing quote
        # Pattern: id="PART"  -> id="PARTsuffix"
        # We need to modify the tag string
        start = m.group(0)
        # Extract the original id
        original_id = m.group('id')
        new_id = original_id + clean_suffix
        # Rebuild the tag with the new id
        new_tag = start.replace(f'id="{original_id}"', f'id="{new_id}"')
        # Now remove the escaped suffix from the new_tag? Actually we replaced the whole match.
        # Better: return only the fixed tag, discarding the escaped suffix.
        return f'{{% include embed/youtube.html id="{new_id}" %}}'
    return BROKEN_TAG_RE.sub(merge, text)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    original = original.lstrip('\ufeff')

    # Backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(original)

    modified = fix_broken(original)

    if modified != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"✅ Fixed: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  No broken tags: {os.path.basename(filepath)}")

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
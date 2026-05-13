#!/usr/bin/env python3
"""
Fix broken Liquid YouTube tags where part of the ID is stuck directly
after the closing '%}' without a space.
Example: {% include embed/youtube.html id="r_" %}dMleOT-Rc
      -> {% include embed/youtube.html id="r_dMleOT-Rc" %}
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"

# Pattern to locate a YouTube Liquid include and capture its id
TAG_RE = re.compile(
    r'\{%\s*include\s+embed/youtube\.html\s+id="(?P<id>[^"]*)"\s*%\}'
)

def merge_stuck_fragments(text):
    """Find broken tags and absorb adjacent word fragments into the ID."""
    result = []
    last_end = 0
    for m in TAG_RE.finditer(text):
        start, end = m.start(), m.end()
        # Append everything before this match
        result.append(text[last_end:start])

        tag_text = m.group(0)
        original_id = m.group('id')

        # Check characters immediately after the closing '%}'
        after_text = text[end:]
        if after_text:
            # If next character is a word character (letter, digit, _, -)
            if after_text[0].isalnum() or after_text[0] in ('_', '-'):
                # Capture the whole adjacent token (until non-word char, but allow hyphen/underscore)
                token_match = re.match(r'[A-Za-z0-9_\\-]+', after_text)
                if token_match:
                    fragment = token_match.group(0)
                    # Remove backslashes (if any) from the fragment
                    fragment_clean = fragment.replace('\\', '')
                    # Merge into the ID
                    new_id = original_id + fragment_clean
                    # Build new tag
                    new_tag = tag_text.replace(f'id="{original_id}"', f'id="{new_id}"')
                    # Advance the position past the fragment
                    last_end = end + len(fragment)
                    # Append the fixed tag
                    result.append(new_tag)
                    # Skip the normal appending of the original tag
                    continue
        # No adjacent fragment – keep the tag as-is
        result.append(tag_text)
        last_end = end

    # Append any remaining text after the last match
    result.append(text[last_end:])
    return ''.join(result)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    original = original.lstrip('\ufeff')

    # Backup
    with open(filepath + '.bak', 'w', encoding='utf-8') as f:
        f.write(original)

    modified = merge_stuck_fragments(original)

    if modified != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"✅ Fixed: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  No stuck fragments: {os.path.basename(filepath)}")

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
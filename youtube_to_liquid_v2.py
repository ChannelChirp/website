#!/usr/bin/env python3
"""
Convert YouTube links in Markdown posts to Liquid include tags.
Now handles Markdown escapes like \_ and \- inside video IDs.
Creates .bak backups.
"""

import os
import re

POSTS_DIR = "_posts"

# Updated regex: allow backslash in the ID (Markdown escape)
YOUTUBE_URL_RE = re.compile(
    r'(?P<url>'
    r'https?://(?:www\.)?'
    r'(?:youtube\.com/watch\?v='
    r'|youtu\.be/'
    r')(?P<id>[A-Za-z0-9_\-\\]+)'   # <-- added backslash
    r'(?:[&?#][^\s<>"\']*)?'        # optional extra params
    r')'
)

# Markdown link [text](url)
MD_LINK_RE = re.compile(r'\[(?P<text>[^\]]*)\]\((?P<url>[^\)]+)\)')

# HTML link <a href="url">text</a>
HTML_LINK_RE = re.compile(
    r'<a\s[^>]*href\s*=\s*"(?P<url>[^"]*)"[^>]*>(?P<text>.*?)</a>',
    re.IGNORECASE
)

def clean_video_id(raw_id):
    """Remove Markdown escape backslashes from the ID."""
    # Remove every backslash (safe because YouTube IDs never contain real backslashes)
    return raw_id.replace('\\', '')

def process_content(text):
    """Replace all YouTube links with Liquid include, return modified text."""

    # 1. Markdown links: [text](url)
    def replace_md_link(m):
        url = m.group('url')
        yt_match = YOUTUBE_URL_RE.search(url)
        if yt_match:
            vid = clean_video_id(yt_match.group('id'))
            return '{% include embed/youtube.html id="' + vid + '" %}'
        return m.group(0)

    text = MD_LINK_RE.sub(replace_md_link, text)

    # 2. HTML links: <a href="...">text</a>
    def replace_html_link(m):
        url = m.group('url')
        yt_match = YOUTUBE_URL_RE.search(url)
        if yt_match:
            vid = clean_video_id(yt_match.group('id'))
            return '{% include embed/youtube.html id="' + vid + '" %}'
        return m.group(0)

    text = HTML_LINK_RE.sub(replace_html_link, text)

    # 3. Plain YouTube URLs (not inside a link)
    def replace_plain_url(m):
        vid = clean_video_id(m.group('id'))
        return '{% include embed/youtube.html id="' + vid + '" %}'

    text = YOUTUBE_URL_RE.sub(replace_plain_url, text)

    return text

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
        print(f"✅ Converted: {os.path.basename(filepath)}")
    else:
        print(f"⏺️  No YouTube links: {os.path.basename(filepath)}")

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
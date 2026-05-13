#!/usr/bin/env python3
"""
Remove existing categories from Jekyll post front matter and
add `categories: adventures`.
- Modifies all .md files in a given directory (default: _posts)
- Creates backup files with .bak extension
"""

import os
import sys
import frontmatter

POSTS_DIR = "_posts"          # change if your posts are elsewhere
REMOVE_KEYS = ["categories", "category"]   # both singular and plural
NEW_CATEGORY = "adventures"

def update_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    changed = False

    # Remove existing category keys
    for key in REMOVE_KEYS:
        if key in post.metadata:
            del post.metadata[key]
            changed = True

    # Add the new categories list
    post.metadata["categories"] = NEW_CATEGORY
    changed = True  # always set, even if it was already "adventures"

    # Write back only if something changed
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))
        print(f"Updated: {filepath}")
    else:
        print(f"No change: {filepath}")

def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"Directory '{POSTS_DIR}' not found.", file=sys.stderr)
        sys.exit(1)

    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    if not md_files:
        print("No Markdown files found.")
        return

    for filename in sorted(md_files):
        filepath = os.path.join(POSTS_DIR, filename)
        # Create a backup
        backup = filepath + ".bak"
        with open(filepath, "rb") as f_src, open(backup, "wb") as f_dst:
            f_dst.write(f_src.read())
        update_post(filepath)

    print(f"\nAll done. Backups saved as .bak files inside '{POSTS_DIR}'.")

if __name__ == "__main__":
    main()
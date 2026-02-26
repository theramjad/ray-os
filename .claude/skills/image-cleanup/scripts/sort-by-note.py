#!/usr/bin/env python3
"""
sort-by-note.py — Reorganize images into per-note subfolders.

Target format: images/{note-slug}/{image-name}.png

Handles:
  - Explicit refs:  ![[images/file.png]]      → resolved relative to folder root
  - Bare refs:      ![[file.png]]              → resolved by searching folder recursively
  - Recursive md:   .md files in subdirectories are scanned too

Usage:
    python3 sort-by-note.py /path/to/folder           # dry run
    python3 sort-by-note.py /path/to/folder --execute # apply changes
"""

import sys
import re
import shutil
from pathlib import Path


def slugify(name):
    """Convert filename to slug: lowercase, non-alphanumeric runs to hyphens."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name


def resolve_ref(folder, ref):
    """
    Resolve an image ref to an absolute path.
    1. Try folder / ref directly (explicit path like images/foo.png)
    2. Fall back to recursive search by filename (bare ref like foo.png)
    Returns Path or None.
    """
    direct = folder / ref
    if direct.exists():
        return direct

    # Bare filename — search recursively, skip .obsidian and .claude
    name = Path(ref).name
    for candidate in folder.rglob(name):
        parts = candidate.parts
        if '.obsidian' in parts or '.claude' in parts:
            continue
        return candidate

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: sort-by-note.py <folder> [--execute]")
        sys.exit(1)

    folder = Path(sys.argv[1])
    execute = '--execute' in sys.argv

    if not folder.is_dir():
        print(f"Error: {folder} is not a directory")
        sys.exit(1)

    # Scan md files recursively, skip hidden dirs
    md_files = [
        p for p in folder.rglob('*.md')
        if '.obsidian' not in p.parts and '.claude' not in p.parts
    ]
    print(f"Found {len(md_files)} markdown file(s)")

    # Build index of all image files in folder for fast duplicate detection
    # maps absolute path → True
    moves = []

    for md_file in md_files:
        note_slug = slugify(md_file.stem)
        content = md_file.read_text(encoding='utf-8')
        refs = re.findall(r'!\[\[([^\]]+)\]\]', content)

        for ref in refs:
            # Only process image extensions
            suffix = Path(ref).suffix.lower()
            if suffix not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}:
                continue

            img_path = resolve_ref(folder, ref)
            if img_path is None:
                print(f"  [MISSING] {ref} (in {md_file.name})")
                continue

            img_name = img_path.name
            target_rel = f"images/{note_slug}/{img_name}"
            target_abs = folder / target_rel

            current_rel = str(img_path.relative_to(folder))
            if current_rel == target_rel:
                continue  # already correct

            moves.append({
                'src': img_path,
                'dst': target_abs,
                'md_file': md_file,
                'old_ref': ref,
                'new_ref': target_rel,
            })

    if not moves:
        print("All images already in correct locations.")
        return

    # Display plan grouped by note
    by_file = {}
    for m in moves:
        by_file.setdefault(m['md_file'].name, []).append(m)

    print(f"\nMOVE PLAN ({len(moves)} image(s) across {len(by_file)} note(s)):")
    for fname, file_moves in sorted(by_file.items()):
        print(f"\n  {fname}:")
        for m in file_moves:
            print(f"    {m['old_ref']}")
            print(f"      → {m['new_ref']}")

    if not execute:
        print("\nDRY RUN — no changes made. Pass --execute to apply.")
        return

    # Deduplicate file moves by source path
    seen_srcs = {}
    for m in moves:
        key = str(m['src'])
        if key not in seen_srcs:
            seen_srcs[key] = m

    # Move files
    moved = 0
    for m in seen_srcs.values():
        m['dst'].parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(m['src']), str(m['dst']))
        moved += 1

    # Update markdown files
    updated_files = set()
    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8')
        new_content = content
        for m in moves:
            if m['md_file'] == md_file:
                new_content = new_content.replace(
                    f'![[{m["old_ref"]}]]',
                    f'![[{m["new_ref"]}]]'
                )
        if new_content != content:
            md_file.write_text(new_content, encoding='utf-8')
            updated_files.add(md_file.name)

    # Remove empty directories
    for dirpath in sorted(folder.rglob('*'), reverse=True):
        if dirpath.is_dir() and dirpath != folder and not any(dirpath.iterdir()):
            dirpath.rmdir()
            print(f"Removed empty directory: {dirpath.relative_to(folder)}")

    print(f"\nMoved {moved} image(s)")
    print(f"Updated {len(updated_files)} markdown file(s): {', '.join(sorted(updated_files))}")
    print("Done!")


if __name__ == '__main__':
    main()

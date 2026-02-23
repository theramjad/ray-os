#!/usr/bin/env python3
"""Download YouTube transcript(s) as plain text files.

Usage:
    python download_transcript.py <video_id_or_url> [video_id_or_url ...] [--out-dir DIR] [--by-channel]

Each transcript is saved as <video_id>.txt in the output directory (default: current directory).
With --by-channel, transcripts are organized into channel-name subfolders.
"""

import argparse
import json
import os
import re
import subprocess
import sys

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(value: str) -> str:
    """Extract a YouTube video ID from a URL or return the value as-is."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    # Assume it's already a video ID
    if re.match(r"^[A-Za-z0-9_-]{11}$", value):
        return value
    print(f"Warning: '{value}' doesn't look like a valid video ID or URL", file=sys.stderr)
    return value


def slugify_channel(name: str) -> str:
    """Convert a channel name to a filesystem-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[''']", "", slug)  # Remove apostrophes
    slug = re.sub(r"[^a-z0-9]+", "-", slug)  # Replace non-alphanumeric with hyphens
    slug = slug.strip("-")
    return slug


def get_channel_name(video_id: str) -> str | None:
    """Fetch channel name for a video using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "%(channel)s", "--skip-download",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def download_transcript(video_id: str, out_dir: str, by_channel: bool = False) -> str:
    """Download transcript for a single video. Returns output path."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    text = "\n".join(entry.text for entry in transcript)

    target_dir = out_dir
    if by_channel:
        channel = get_channel_name(video_id)
        if channel:
            slug = slugify_channel(channel)
            target_dir = os.path.join(out_dir, slug)
            print(f"  Channel: {channel} -> {slug}/")
        else:
            print(f"  Warning: couldn't fetch channel name, saving to root dir", file=sys.stderr)

    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, f"{video_id}.txt")
    with open(out_path, "w") as f:
        f.write(text)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Download YouTube transcripts")
    parser.add_argument("videos", nargs="+", help="Video IDs or YouTube URLs")
    parser.add_argument("--out-dir", default=".", help="Output directory (default: current dir)")
    parser.add_argument("--by-channel", action="store_true",
                        help="Organize transcripts into channel-name subfolders")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for value in args.videos:
        video_id = extract_video_id(value)
        print(f"Downloading transcript for {video_id}...")
        try:
            out_path = download_transcript(video_id, args.out_dir, args.by_channel)
            print(f"  Saved to {out_path}")
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

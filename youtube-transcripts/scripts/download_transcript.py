#!/usr/bin/env python3
"""Download YouTube transcript(s) as plain text files.

Usage:
    python download_transcript.py <video_id_or_url> [video_id_or_url ...] [--out-dir DIR]

Each transcript is saved as <video_id>.txt in the output directory (default: current directory).
"""

import argparse
import os
import re
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


def download_transcript(video_id: str, out_dir: str) -> str:
    """Download transcript for a single video. Returns output path."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    text = "\n".join(entry.text for entry in transcript)
    out_path = os.path.join(out_dir, f"{video_id}.txt")
    with open(out_path, "w") as f:
        f.write(text)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Download YouTube transcripts")
    parser.add_argument("videos", nargs="+", help="Video IDs or YouTube URLs")
    parser.add_argument("--out-dir", default=".", help="Output directory (default: current dir)")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for value in args.videos:
        video_id = extract_video_id(value)
        print(f"Downloading transcript for {video_id}...")
        try:
            out_path = download_transcript(video_id, args.out_dir)
            print(f"  Saved to {out_path}")
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

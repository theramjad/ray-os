---
name: youtube-transcripts
description: Download YouTube video transcripts as plain text files. Use when the user asks to download, fetch, or save transcripts/captions/subtitles from YouTube videos. Accepts video IDs or full YouTube URLs.
---

# YouTube Transcripts

Download YouTube transcripts using `scripts/download_transcript.py`. Transcripts are automatically organized into channel-name subfolders.

## Usage

```bash
python3 <skill-dir>/scripts/download_transcript.py <video_id_or_url> [more...] [--out-dir DIR]
```

- Accepts YouTube video IDs (`pb0lVGDiigI`) or full URLs (`https://youtube.com/watch?v=pb0lVGDiigI`)
- Automatically organizes transcripts into channel-name subfolders via `yt-dlp`
- Default output directory is the current working directory

## Examples

Single video:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI --out-dir transcripts/
```

Output:
```
transcripts/
└── ray-amjad/
    └── pb0lVGDiigI.txt
```

Multiple videos:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI mZzhfPle9QU --out-dir transcripts/
```

Output:
```
transcripts/
├── ray-amjad/
│   └── pb0lVGDiigI.txt
└── john-kim/
    └── mZzhfPle9QU.txt
```

## Requirements

- Python 3
- `youtube-transcript-api` package (`pip install youtube-transcript-api`)
- `yt-dlp` (for channel name lookup)

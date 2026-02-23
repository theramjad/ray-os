---
name: youtube-transcripts
description: Download YouTube video transcripts as plain text files. Use when the user asks to download, fetch, or save transcripts/captions/subtitles from YouTube videos. Accepts video IDs or full YouTube URLs.
---

# YouTube Transcripts

Download YouTube transcripts using `scripts/download_transcript.py`.

## Usage

```bash
python3 <skill-dir>/scripts/download_transcript.py <video_id_or_url> [more...] [--out-dir DIR] [--by-channel]
```

- Accepts YouTube video IDs (`pb0lVGDiigI`) or full URLs (`https://youtube.com/watch?v=pb0lVGDiigI`)
- Saves each transcript as `<video_id>.txt` in the output directory
- Default output directory is the current working directory
- `--by-channel` organizes transcripts into channel-name subfolders (requires `yt-dlp`)

## Examples

Single video:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI --out-dir transcripts/
```

Multiple videos grouped by channel:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI mZzhfPle9QU --out-dir transcripts/ --by-channel
```

This creates:
```
transcripts/
├── ray-amjad/
│   └── pb0lVGDiigI.txt
└── john-kim/
    └── mZzhfPle9QU.txt
```

## Default behavior

**Always use `--by-channel`** when downloading transcripts to keep them organized. The channel name is fetched via `yt-dlp` and slugified (e.g., "John Kim" -> `john-kim/`).

## Requirements

- Python 3
- `youtube-transcript-api` package (`pip install youtube-transcript-api`)
- `yt-dlp` (for `--by-channel` feature)

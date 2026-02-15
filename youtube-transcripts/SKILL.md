---
name: youtube-transcripts
description: Download YouTube video transcripts as plain text files. Use when the user asks to download, fetch, or save transcripts/captions/subtitles from YouTube videos. Accepts video IDs or full YouTube URLs.
---

# YouTube Transcripts

Download YouTube transcripts using `scripts/download_transcript.py`.

## Usage

```bash
python3 <skill-dir>/scripts/download_transcript.py <video_id_or_url> [more...] [--out-dir DIR]
```

- Accepts YouTube video IDs (`pb0lVGDiigI`) or full URLs (`https://youtube.com/watch?v=pb0lVGDiigI`)
- Saves each transcript as `<video_id>.txt` in the output directory
- Default output directory is the current working directory

## Examples

Single video:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI --out-dir transcripts/
```

Multiple videos:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI IiA4Ku5viyg rXTvax9pyhs --out-dir transcripts/
```

From URL:
```bash
python3 scripts/download_transcript.py "https://www.youtube.com/watch?v=pb0lVGDiigI"
```

## Requirements

- Python 3
- `youtube-transcript-api` package (`pip install youtube-transcript-api`)

#!/usr/bin/env python3
"""Extract audio from MP4 and transcribe via Deepgram Nova-3 with word-level timestamps.

Output format is compatible with the AssemblyAI transcript JSON used by format_transcript.py,
so the same downstream pipeline works with either provider.

Usage:
    python3 transcribe_deepgram.py <input.mp4> --api-key <key>
    python3 transcribe_deepgram.py <input.mp4>   # uses DEEPGRAM_API_KEY env var
    python3 transcribe_deepgram.py <input.mp3> --skip-extract
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error


def extract_audio(mp4_path, mp3_path):
    """Extract audio from MP4 to MP3 using ffmpeg."""
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path]
    print(f"Extracting audio: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Audio extracted to {mp3_path}")


def transcribe_deepgram(audio_path, api_key):
    """Send audio to Deepgram Nova-3 and return the full response."""
    url = (
        "https://api.deepgram.com/v1/listen?"
        "model=nova-3&language=en&smart_format=true&"
        "punctuate=true&filler_words=true&utterances=true"
    )

    # Determine content type
    ext = os.path.splitext(audio_path)[1].lower()
    content_types = {
        ".mp3": "audio/mpeg",
        ".mp4": "audio/mp4",
        ".wav": "audio/wav",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
    }
    content_type = content_types.get(ext, "audio/mpeg")

    file_size = os.path.getsize(audio_path)
    print(f"Uploading {audio_path} ({file_size / 1024 / 1024:.1f} MB) to Deepgram Nova-3...")

    with open(audio_path, "rb") as f:
        data = f.read()

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Token {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Deepgram API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    print("Transcription complete.")
    return result


def convert_to_assemblyai_format(deepgram_result):
    """Convert Deepgram response to AssemblyAI-compatible word list.

    AssemblyAI format: {"words": [{"text": str, "start": int_ms, "end": int_ms, "confidence": float}, ...]}
    Deepgram format: results.channels[0].alternatives[0].words[{word, start, end, confidence, punctuated_word}]
    """
    dg_words = deepgram_result["results"]["channels"][0]["alternatives"][0]["words"]

    words = []
    for w in dg_words:
        words.append({
            "text": w.get("punctuated_word", w["word"]),
            "start": int(round(w["start"] * 1000)),  # seconds -> ms
            "end": int(round(w["end"] * 1000)),       # seconds -> ms
            "confidence": w.get("confidence", 0.0),
        })

    return {"words": words, "_provider": "deepgram", "_model": "nova-3"}


def main():
    parser = argparse.ArgumentParser(description="Extract audio and transcribe with Deepgram Nova-3")
    parser.add_argument("input", help="Path to input MP4 or audio file")
    parser.add_argument("-o", "--output", help="Path for output JSON (default: <basename>_transcript_deepgram.json)")
    parser.add_argument("--api-key", help="Deepgram API key (or set DEEPGRAM_API_KEY env var)")
    parser.add_argument("--skip-extract", action="store_true", help="Skip audio extraction (input is already audio)")
    parser.add_argument("--mp3", help="Path to MP3 (default: <basename>.mp3)")
    parser.add_argument("--raw", action="store_true", help="Also save raw Deepgram response")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set DEEPGRAM_API_KEY env var", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(args.input)[0]
    mp3_path = args.mp3 or f"{base}.mp3"
    output_path = args.output or f"{base}_transcript_deepgram.json"

    # Extract audio if input is MP4
    audio_path = args.input
    if not args.skip_extract and args.input.lower().endswith(".mp4"):
        extract_audio(args.input, mp3_path)
        audio_path = mp3_path

    # Transcribe
    raw_result = transcribe_deepgram(audio_path, api_key)

    # Save raw response if requested
    if args.raw:
        raw_path = f"{base}_deepgram_raw.json"
        with open(raw_path, "w") as f:
            json.dump(raw_result, f, indent=2)
        print(f"Raw Deepgram response saved to {raw_path}")

    # Convert to AssemblyAI-compatible format
    result = convert_to_assemblyai_format(raw_result)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    duration = raw_result.get("metadata", {}).get("duration", 0)
    print(f"Transcript saved to {output_path}")
    print(f"Word count: {len(result['words'])}")
    print(f"Audio duration: {duration:.1f}s ({duration/60:.1f}min)")


if __name__ == "__main__":
    main()

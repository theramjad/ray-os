#!/usr/bin/env python3
"""Extract audio from MP4 and transcribe via AssemblyAI with word-level timestamps."""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error


def extract_audio(mp4_path: str, mp3_path: str) -> None:
    """Extract audio from MP4 to MP3 using ffmpeg."""
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path]
    print(f"Extracting audio: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Audio extracted to {mp3_path}")


def upload_audio(mp3_path: str, api_key: str) -> str:
    """Upload audio file to AssemblyAI and return the upload URL."""
    print(f"Uploading {mp3_path} to AssemblyAI...")
    with open(mp3_path, "rb") as f:
        data = f.read()

    req = urllib.request.Request(
        "https://api.assemblyai.com/v2/upload",
        data=data,
        headers={"authorization": api_key, "content-type": "application/octet-stream"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    print(f"Upload complete: {result['upload_url']}")
    return result["upload_url"]


def request_transcription(upload_url: str, api_key: str) -> str:
    """Request transcription and return transcript ID."""
    payload = json.dumps({
        "audio_url": upload_url,
        "speech_models": ["universal-3-pro", "universal-2"],
        "language_code": "en",
    }).encode()
    req = urllib.request.Request(
        "https://api.assemblyai.com/v2/transcript",
        data=payload,
        headers={"authorization": api_key, "content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    print(f"Transcription requested: {result['id']}")
    return result["id"]


def poll_transcription(transcript_id: str, api_key: str) -> dict:
    """Poll until transcription completes and return full result."""
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    while True:
        req = urllib.request.Request(url, headers={"authorization": api_key})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
        status = result["status"]
        if status == "completed":
            print("Transcription complete.")
            return result
        elif status == "error":
            print(f"Transcription failed: {result.get('error', 'unknown')}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Status: {status} — waiting 5s...")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Extract audio and transcribe with AssemblyAI")
    parser.add_argument("mp4", help="Path to input MP4 file")
    parser.add_argument("-o", "--output", help="Path for output JSON (default: <mp4_basename>_transcript.json)")
    parser.add_argument("--api-key", help="AssemblyAI API key (or set ASSEMBLYAI_API_KEY env var)")
    parser.add_argument("--skip-extract", action="store_true", help="Skip audio extraction (use existing MP3)")
    parser.add_argument("--mp3", help="Path to MP3 (default: <mp4_basename>.mp3)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set ASSEMBLYAI_API_KEY env var", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(args.mp4)[0]
    mp3_path = args.mp3 or f"{base}.mp3"
    output_path = args.output or f"{base}_transcript.json"

    if not args.skip_extract:
        extract_audio(args.mp4, mp3_path)

    upload_url = upload_audio(mp3_path, api_key)
    transcript_id = request_transcription(upload_url, api_key)
    result = poll_transcription(transcript_id, api_key)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Transcript saved to {output_path}")
    print(f"Word count: {len(result.get('words', []))}")


if __name__ == "__main__":
    main()

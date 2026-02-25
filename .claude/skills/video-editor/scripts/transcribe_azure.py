#!/usr/bin/env python3
"""Extract audio from MP4 and transcribe via Azure Speech Fast Transcription API.

Output format is compatible with the AssemblyAI transcript JSON used by format_transcript.py,
so the same downstream pipeline works with any provider.

Usage:
    python3 transcribe_azure.py <input.mp4> --api-key <key> --region japaneast
    python3 transcribe_azure.py <input.mp3> --skip-extract --api-key <key> --region japaneast
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


def transcribe_azure(audio_path, api_key, region, locale="en-US"):
    """Send audio to Azure Fast Transcription API and return the response."""
    api_version = "2024-11-15"
    url = (
        f"https://{region}.api.cognitive.microsoft.com"
        f"/speechtotext/transcriptions:transcribe"
        f"?api-version={api_version}"
    )

    file_size = os.path.getsize(audio_path)
    print(f"Uploading {audio_path} ({file_size / 1024 / 1024:.1f} MB) to Azure Speech ({region})...")

    # Build multipart form data manually
    boundary = "----AzureSpeechBoundary9876543210"

    definition = json.dumps({"locales": [locale]})

    body_parts = []
    # Definition part
    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Disposition: form-data; name="definition"\r\n')
    body_parts.append(b'Content-Type: application/json\r\n\r\n')
    body_parts.append(definition.encode())
    body_parts.append(b'\r\n')

    # Audio file part
    filename = os.path.basename(audio_path)
    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(f'Content-Disposition: form-data; name="audio"; filename="{filename}"\r\n'.encode())
    body_parts.append(b'Content-Type: application/octet-stream\r\n\r\n')
    with open(audio_path, "rb") as f:
        body_parts.append(f.read())
    body_parts.append(b'\r\n')
    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode() if e.fp else ""
        print(f"Azure API error {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)

    print("Transcription complete.")
    return result


def convert_to_assemblyai_format(azure_result):
    """Convert Azure Fast Transcription response to AssemblyAI-compatible word list.

    Azure format: phrases[].words[{text, offsetMilliseconds, durationMilliseconds}]
    Output format: {words: [{text, start, end, confidence}, ...]}
    """
    words = []
    for phrase in azure_result.get("phrases", []):
        for w in phrase.get("words", []):
            words.append({
                "text": w["text"],
                "start": w["offsetMilliseconds"],
                "end": w["offsetMilliseconds"] + w["durationMilliseconds"],
                "confidence": phrase.get("confidence", 0.0),
            })

    duration = azure_result.get("durationMilliseconds", 0)
    return {"words": words, "_provider": "azure", "_model": "fast-transcription", "_duration_ms": duration}


def main():
    parser = argparse.ArgumentParser(description="Extract audio and transcribe with Azure Speech")
    parser.add_argument("input", help="Path to input MP4 or audio file")
    parser.add_argument("-o", "--output", help="Path for output JSON (default: <basename>_transcript_azure.json)")
    parser.add_argument("--api-key", help="Azure Speech API key (or set AZURE_SPEECH_API_KEY env var)")
    parser.add_argument("--region", default="japaneast", help="Azure region (default: japaneast)")
    parser.add_argument("--skip-extract", action="store_true", help="Skip audio extraction (input is already audio)")
    parser.add_argument("--mp3", help="Path to MP3 (default: <basename>.mp3)")
    parser.add_argument("--raw", action="store_true", help="Also save raw Azure response")
    parser.add_argument("--locale", default="en-US", help="Locale (default: en-US)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("AZURE_SPEECH_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set AZURE_SPEECH_API_KEY env var", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(args.input)[0]
    mp3_path = args.mp3 or f"{base}.mp3"
    output_path = args.output or f"{base}_transcript_azure.json"

    # Extract audio if input is MP4
    audio_path = args.input
    if not args.skip_extract and args.input.lower().endswith(".mp4"):
        extract_audio(args.input, mp3_path)
        audio_path = mp3_path

    # Transcribe
    raw_result = transcribe_azure(audio_path, api_key, args.region, args.locale)

    # Save raw response if requested
    if args.raw:
        raw_path = f"{base}_azure_raw.json"
        with open(raw_path, "w") as f:
            json.dump(raw_result, f, indent=2)
        print(f"Raw Azure response saved to {raw_path}")

    # Convert to AssemblyAI-compatible format
    result = convert_to_assemblyai_format(raw_result)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    duration = raw_result.get("durationMilliseconds", 0)
    print(f"Transcript saved to {output_path}")
    print(f"Word count: {len(result['words'])}")
    print(f"Audio duration: {duration/1000:.1f}s ({duration/60000:.1f}min)")


if __name__ == "__main__":
    main()

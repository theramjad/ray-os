#!/usr/bin/env python3
"""Extract audio from MP4 and transcribe via Google Cloud Speech-to-Text V1.

Uses longrunningrecognize with word-level timestamps. Requires a GCS bucket for
files >10MB, so the script uploads to a temp GCS location, transcribes, and cleans up.

Output format is compatible with the AssemblyAI transcript JSON used by format_transcript.py.

Usage:
    python3 transcribe_google.py <input.mp4> --credentials /path/to/service-account.json
    python3 transcribe_google.py <input.mp3> --skip-extract --credentials key.json --bucket my-bucket
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error


def extract_audio(mp4_path, mp3_path):
    """Extract audio from MP4 to MP3 using ffmpeg."""
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path]
    print(f"Extracting audio: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Audio extracted to {mp3_path}")


def get_access_token(credentials_path):
    """Get an OAuth2 access token from a service account JSON key."""
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    scopes = [
        "https://www.googleapis.com/auth/cloud-platform",
    ]
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )
    creds.refresh(Request())
    return creds.token, creds.project_id


def api_request(url, method="GET", data=None, headers=None, content_type=None, timeout=600):
    """Make an HTTP request and return parsed JSON."""
    if data and isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
    elif data and isinstance(data, str):
        data = data.encode()

    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    if content_type:
        req.add_header("Content-Type", content_type)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"API error {e.code}: {body}", file=sys.stderr)
        raise


def ensure_bucket(project_id, bucket_name, token):
    """Create a GCS bucket if it doesn't exist."""
    headers = {"Authorization": f"Bearer {token}"}

    # Check if bucket exists
    try:
        api_request(
            f"https://storage.googleapis.com/storage/v1/b/{bucket_name}",
            headers=headers,
        )
        print(f"Using existing bucket: {bucket_name}")
        return
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    # Create bucket
    print(f"Creating bucket: {bucket_name}")
    api_request(
        f"https://storage.googleapis.com/storage/v1/b?project={project_id}",
        method="POST",
        data={"name": bucket_name, "location": "US"},
        headers=headers,
        content_type="application/json",
    )
    print(f"Bucket created: {bucket_name}")


def upload_to_gcs(local_path, bucket_name, object_name, token):
    """Upload a file to GCS."""
    file_size = os.path.getsize(local_path)
    print(f"Uploading {local_path} ({file_size / 1024 / 1024:.1f} MB) to gs://{bucket_name}/{object_name}...")

    with open(local_path, "rb") as f:
        data = f.read()

    url = (
        f"https://storage.googleapis.com/upload/storage/v1/b/{bucket_name}"
        f"/o?uploadType=media&name={object_name}"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/mpeg",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=600) as resp:
        result = json.loads(resp.read().decode())

    print(f"Upload complete: gs://{bucket_name}/{object_name}")
    return f"gs://{bucket_name}/{object_name}"


def delete_from_gcs(bucket_name, object_name, token):
    """Delete an object from GCS."""
    url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{object_name}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        req = urllib.request.Request(url, headers=headers, method="DELETE")
        urllib.request.urlopen(req, timeout=30)
        print(f"Deleted gs://{bucket_name}/{object_name}")
    except urllib.error.HTTPError:
        print(f"Warning: could not delete gs://{bucket_name}/{object_name}")


def transcribe_google(gcs_uri, token):
    """Start a longrunningrecognize request and return the operation name."""
    url = "https://speech.googleapis.com/v1/speech:longrunningrecognize"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "config": {
            "encoding": "MP3",
            "languageCode": "en-US",
            "enableWordTimeOffsets": True,
            "enableAutomaticPunctuation": True,
            "model": "latest_long",
        },
        "audio": {
            "uri": gcs_uri,
        },
    }

    print("Starting transcription...")
    result = api_request(url, method="POST", data=payload, headers=headers, content_type="application/json")
    op_name = result["name"]
    print(f"Operation started: {op_name}")
    return op_name


def poll_operation(op_name, token, poll_interval=5):
    """Poll a long-running operation until completion."""
    url = f"https://speech.googleapis.com/v1/operations/{op_name}"
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        result = api_request(url, headers=headers)
        if result.get("done"):
            if "error" in result:
                print(f"Transcription failed: {result['error']}", file=sys.stderr)
                sys.exit(1)
            print("Transcription complete.")
            return result["response"]

        progress = result.get("metadata", {}).get("progressPercent", 0)
        print(f"Progress: {progress}% — waiting {poll_interval}s...")
        time.sleep(poll_interval)


def parse_duration_string(s):
    """Parse Google's duration string like '1.400s' to milliseconds."""
    return int(round(float(s.rstrip("s")) * 1000))


def convert_to_assemblyai_format(google_response):
    """Convert Google STT response to AssemblyAI-compatible word list."""
    words = []
    for result in google_response.get("results", []):
        alt = result.get("alternatives", [{}])[0]
        for w in alt.get("words", []):
            words.append({
                "text": w["word"],
                "start": parse_duration_string(w["startTime"]),
                "end": parse_duration_string(w["endTime"]),
                "confidence": alt.get("confidence", 0.0),
            })

    return {"words": words, "_provider": "google", "_model": "latest_long"}


def main():
    parser = argparse.ArgumentParser(description="Extract audio and transcribe with Google Cloud STT")
    parser.add_argument("input", help="Path to input MP4 or audio file")
    parser.add_argument("-o", "--output", help="Output JSON path (default: <basename>_transcript_google.json)")
    parser.add_argument("--credentials", required=True, help="Path to service account JSON key")
    parser.add_argument("--bucket", help="GCS bucket name (default: <project_id>-speech-temp)")
    parser.add_argument("--skip-extract", action="store_true", help="Skip audio extraction")
    parser.add_argument("--mp3", help="Path to MP3 (default: <basename>.mp3)")
    parser.add_argument("--raw", action="store_true", help="Also save raw Google response")
    parser.add_argument("--keep-gcs", action="store_true", help="Don't delete the uploaded file from GCS")
    args = parser.parse_args()

    base = os.path.splitext(args.input)[0]
    mp3_path = args.mp3 or f"{base}.mp3"
    output_path = args.output or f"{base}_transcript_google.json"

    # Get access token
    print("Authenticating with Google Cloud...")
    token, project_id = get_access_token(args.credentials)
    print(f"Project: {project_id}")

    bucket_name = args.bucket or f"{project_id}-speech-temp"

    # Extract audio if needed
    audio_path = args.input
    if not args.skip_extract and args.input.lower().endswith(".mp4"):
        extract_audio(args.input, mp3_path)
        audio_path = mp3_path

    # Ensure bucket exists and upload
    ensure_bucket(project_id, bucket_name, token)
    object_name = f"speech-temp/{os.path.basename(audio_path)}"
    gcs_uri = upload_to_gcs(audio_path, bucket_name, object_name, token)

    try:
        # Transcribe
        op_name = transcribe_google(gcs_uri, token)
        raw_response = poll_operation(op_name, token)

        # Save raw response if requested
        if args.raw:
            raw_path = f"{base}_google_raw.json"
            with open(raw_path, "w") as f:
                json.dump(raw_response, f, indent=2)
            print(f"Raw Google response saved to {raw_path}")

        # Convert to AssemblyAI-compatible format
        result = convert_to_assemblyai_format(raw_response)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Transcript saved to {output_path}")
        print(f"Word count: {len(result['words'])}")

    finally:
        # Clean up GCS
        if not args.keep_gcs:
            delete_from_gcs(bucket_name, object_name, token)


if __name__ == "__main__":
    main()

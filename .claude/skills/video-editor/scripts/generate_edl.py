#!/usr/bin/env python3
"""Generate a CMX 3600 EDL file from an edit decision list JSON.

The EDL can be imported directly into Adobe Premiere Pro, DaVinci Resolve,
or any NLE that supports CMX 3600 format.

Usage:
    python3 generate_edl.py <edl.json> <source.mp4> -o output.edl [--fps 30]

Import in Premiere Pro:
    File > Import > select the .edl file > match frame rate > link source media
"""

import argparse
import json
import os
import subprocess
import sys


def get_fps(mp4_path: str) -> float:
    """Detect frame rate of source video using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "json",
        mp4_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 30.0  # fallback
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    if not streams:
        return 30.0
    # r_frame_rate is like "30/1" or "30000/1001"
    rate_str = streams[0].get("r_frame_rate", "30/1")
    num, den = rate_str.split("/")
    return float(num) / float(den)


def ms_to_timecode(ms: int, fps: int) -> str:
    """Convert milliseconds to HH:MM:SS:FF timecode."""
    total_frames = round(ms * fps / 1000)
    ff = total_frames % fps
    total_seconds = total_frames // fps
    ss = total_seconds % 60
    total_minutes = total_seconds // 60
    mm = total_minutes % 60
    hh = total_minutes // 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def generate_edl(segments, source_name, fps=30, title="Video Edit"):
    """Generate CMX 3600 EDL content string."""
    # Reel name: max 8 chars, uppercase
    reel = os.path.splitext(source_name)[0][:8].upper().replace(" ", "_")
    reel = reel.ljust(8)

    lines = [f"TITLE: {title}", "FCM: NON-DROP FRAME", ""]

    # Timeline starts at 01:00:00:00 (standard convention)
    record_offset_ms = 3_600_000

    for i, seg in enumerate(segments, start=1):
        start_ms = seg["start_ms"]
        end_ms = seg["end_ms"]
        duration_ms = end_ms - start_ms

        src_in = ms_to_timecode(start_ms, fps)
        src_out = ms_to_timecode(end_ms, fps)
        rec_in = ms_to_timecode(record_offset_ms, fps)
        rec_out = ms_to_timecode(record_offset_ms + duration_ms, fps)

        lines.append(
            f"{i:03d}  {reel} AA/V  C        "
            f"{src_in} {src_out} {rec_in} {rec_out}"
        )
        lines.append(f"* FROM CLIP NAME: {source_name}")
        lines.append("")

        record_offset_ms += duration_ms

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Premiere Pro EDL from edit decision list")
    parser.add_argument("edl_json", help="Path to EDL JSON (with segments array)")
    parser.add_argument("source_mp4", help="Path to source MP4 (for reel name and fps detection)")
    parser.add_argument("-o", "--output", help="Output .edl path (default: <basename>.edl)")
    parser.add_argument("--fps", type=int, help="Frame rate (default: auto-detect from source)")
    parser.add_argument("--title", default="Video Edit", help="Sequence title")
    args = parser.parse_args()

    with open(args.edl_json) as f:
        edl_data = json.load(f)

    segments = edl_data.get("segments", [])
    if not segments:
        print("No segments found in EDL JSON.", file=sys.stderr)
        sys.exit(1)

    fps = args.fps or round(get_fps(args.source_mp4))
    print(f"Using {fps} fps")

    source_name = os.path.basename(args.source_mp4)
    edl_content = generate_edl(segments, source_name, fps, args.title)

    output_path = args.output or os.path.splitext(args.edl_json)[0] + ".edl"
    with open(output_path, "w") as f:
        f.write(edl_content)

    total_kept_s = sum((s["end_ms"] - s["start_ms"]) / 1000 for s in segments)
    print(f"EDL saved to {output_path}")
    print(f"{len(segments)} events, {total_kept_s:.1f}s total on timeline")
    print(f"\nImport in Premiere Pro: File > Import > select {os.path.basename(output_path)}")


if __name__ == "__main__":
    main()

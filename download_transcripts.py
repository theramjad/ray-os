#!/usr/bin/env python3
"""Download YouTube transcripts for all tracked videos into transcripts/ folder."""

import os
from youtube_transcript_api import YouTubeTranscriptApi

VIDEOS = {
    "1_opus_prompting_tips": "pb0lVGDiigI",
    "2_weekly_features_update": "IiA4Ku5viyg",
    "3_browser_control_update": "rXTvax9pyhs",
    "4_2026_coding_workflow": "sy65ARFI9Bg",
    "5_subagents_update": "NmKdYlODC24",
    "6_planning_features": "aF4QAHbNDrA",
    "7_task_management": "6omInQipcag",
    "8_agent_swarms": "DWiYdXrxSwg",
}

def download_transcripts():
    os.makedirs("transcripts", exist_ok=True)
    api = YouTubeTranscriptApi()

    for name, video_id in VIDEOS.items():
        out_path = f"transcripts/{name}.txt"
        print(f"Downloading transcript for {name} ({video_id})...")
        try:
            transcript = api.fetch(video_id)
            text = "\n".join(entry.text for entry in transcript)
            with open(out_path, "w") as f:
                f.write(text)
            print(f"  Saved to {out_path}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    download_transcripts()

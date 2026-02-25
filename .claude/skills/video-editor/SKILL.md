---
name: video-editor
description: >
  Edit raw screen recording videos with synced audio. Removes repeated takes, false starts,
  silence, filler, and [MUSIC] tags to produce a clean final cut. Use when the user provides
  a raw/unedited MP4 video file and wants it edited down. Triggers on: "edit this video",
  "cut this video", providing a raw MP4 for editing, or any request to remove bad takes
  from a recording.
---

# Video Editor

Edit raw screen recordings by transcribing, reviewing the transcript as an LLM editor,
and applying cuts with ffmpeg.

## Pipeline

```
MP4 → AssemblyAI (transcribe) → Claude (editorial decisions) → refine_edl.py (VAD) → ffmpeg (cut + join) → edited MP4
```

### Step 1: Transcribe

```bash
python3 <skill_dir>/scripts/transcribe_assemblyai.py <input.mp4> --api-key <key>
```

Requires `ASSEMBLYAI_API_KEY` env var or `--api-key` flag.
Uses AssemblyAI `universal-3-pro` model with English language.
Word-level timestamps are returned by default.
Outputs `<basename>_transcript.json`.

Alternative providers available (`transcribe_deepgram.py`, `transcribe_azure.py`) but
AssemblyAI has the best timestamp accuracy (74ms avg vs 135ms Deepgram, 106ms Azure)
and lowest start bias (+39ms vs +58ms Deepgram, +144ms Azure). Tested against
human-corrected ground truth on a 24min recording with 71 segment boundaries.

### Step 2: Format for review

```bash
python3 <skill_dir>/scripts/format_transcript.py <transcript.json> -o <formatted.txt>
```

Outputs timestamped lines like:
```
[00:08.16 - 00:12.34] Okay, so we have a lot of Cloud Code updates to go over—
[00:12.50 - 00:18.90] Okay, so we have a whole bunch of Cloud Code updates to go...
```

### Step 3: Editorial review (you, the LLM)

Read the formatted transcript top to bottom. A ~24min raw recording produces ~300 lines,
easily reviewable in one pass. Apply these editing rules:

**Last take wins.** When the speaker repeats the same line or phrase multiple times (retakes),
keep only the LAST complete take. Earlier attempts are always cut. Retakes are easy to spot:
consecutive lines starting with the same few words (e.g., 8 lines all starting "First of all,
one of the biggest..."). Always pick the last one that completes the full thought.

**Cut false starts.** Any sentence that trails off mid-thought ending with "—" or just stops
and restarts is cut. Keep only the completed version. A line ending with "—" is almost always
a false start — look for the completed version in the lines that follow. **Exception:** if a
false start contains a useful phrase that the clean retake omits (e.g., "model system card"),
extract that phrase as a micro-segment (even 1-2s) and place it before the clean retake.

**Remove all non-speech.** Every `[MUSIC]`, `[NOISE]`, `[APPLAUSE]`, or similar tag is removed entirely.

**Remove dead air.** Gaps and silence between takes are cut. The final video should flow
continuously from one kept segment to the next. **Also cut silence WITHIN segments** — if a kept
segment has a 500ms+ internal pause (breath, hesitation, dead air), split it into two
segments with the silence removed. Review every segment >5s and look for gaps in the
transcript timestamps. Even short segments can contain splittable pauses.

**Trim filler and stumbles.** Remove standalone filler ("uh", "um", "like", "you know") when they
appear as hesitations. Also surgically remove mid-sentence stumbles by ending a segment before
the stumble and starting a new segment after the correction. Don't keep stumbles just because
splitting feels awkward — the cut always works better than the stumble in the final video.

**Preserve the speaker's intent.** The final edit should read as if the speaker said everything
correctly on the first try. Maintain the logical flow and ordering of topics.

**When in doubt, keep the later version.** If two takes are roughly equal quality, prefer the later one.

**Merge adjacent segments.** When two kept segments are very close together (gap < 300ms),
merge them into one segment rather than creating a cut. This avoids micro-glitches.

### Output format

Produce an EDL (edit decision list) as JSON:

```json
{
  "segments": [
    {"start_ms": 68100, "end_ms": 82700},
    {"start_ms": 121300, "end_ms": 160400}
  ]
}
```

Each segment is a portion of the ORIGINAL video to keep. Segments must be in chronological order
and non-overlapping.

**Padding:** Add ~200ms padding before each segment start (to catch speech onset that
precedes the transcript timestamp). Do NOT over-pad — 400ms was found to be too much,
causing the user to trim most starts back. Add ~200ms after each segment end.
AssemblyAI `start` timestamps mark when a word becomes recognizable (~200-300ms after
the speaker begins the sound), so the start padding compensates for this.

Write the EDL to `<basename>_edl.json`.

### Step 3.5: Refine EDL with silence detection

```bash
python3 <skill_dir>/scripts/refine_edl.py <input.mp4> <edl.json> [-o <refined_edl.json>]
```

Uses ffmpeg `silencedetect` to refine the EDL — no extra Python dependencies.

**Boundary verification:** Extends segment starts/ends outward (up to 300ms) if speech is
detected at the boundary. Prevents the most common issue: clipped word onsets.

**Internal pause splitting:** Finds silence gaps ≥500ms inside segments and splits them.
Catches ~70% of the splits the user would make manually. Segments <500ms created by
splitting are dropped (noise blips between adjacent silences).

Options:
- `--noise-db -35` — silence threshold (lower = more sensitive, default -35)
- `--min-pause-ms 500` — minimum internal silence to split at
- `--extend-ms 300` — max boundary extension
- `--min-segment-ms 500` — drop segments shorter than this after splitting
- `--dry-run` — show changes without writing

### Step 4: Apply edits

```bash
python3 <skill_dir>/scripts/apply_edits.py <input.mp4> <edl.json> -o <output_edited.mp4>
```

Cuts the original MP4 per the EDL and concatenates into the final edit.

### Step 5: Generate Premiere Pro EDL

```bash
python3 <skill_dir>/scripts/generate_edl.py <edl.json> <input.mp4> -o <output.edl>
```

Generates a CMX 3600 `.edl` file importable by Premiere Pro, DaVinci Resolve, and any NLE.
Auto-detects frame rate from the source MP4 via ffprobe.
The user can import via File > Import in Premiere Pro, match frame rate, then link the source media.
All cuts appear as events on a single timeline — ready for final review and polish.

## Handling large transcripts

If the formatted transcript is too long for a single pass (>2000 lines), process it in sections:

1. Read the first ~500 lines, produce keep-segments for that portion.
2. Continue reading the next ~500 lines, noting the overlap context.
3. Merge all segments into one EDL at the end.

In practice: a 24min raw recording = ~3400 words = ~300 formatted lines (one pass).
A 2-hour recording would be ~2500 lines (may need 4-5 passes).

## Quality check

After generating the EDL, run a sanity check:
- Total kept duration should be 30-40% of original for typical recordings with many retakes.
- No segment should be shorter than 500ms (likely a mistake).
- No gap between the end of one segment and start of the next should be < 50ms (merge them).
- Review any segment longer than 5 seconds — it may contain an internal pause to split out.
- Typical result: ~60-75 segments for a 20-25min raw recording (after splitting internal pauses).
- Prefer under-clipping to over-clipping. It's easier for the user to trim excess than to extend clipped speech.
- apply_edits.py takes ~2-3 minutes for ~60 segments (re-encodes each segment).

## Learnings from corrected edits

### Edit 1: 24min recording (58 → 71 segments)
- **0 segments removed** — content selection (what to keep) was 100% correct.
- **12 segments split** — the biggest correction. Long segments (10-20s) contained 1-2s
  internal pauses that should have been cut. Always split segments at internal silence gaps.
- **1 segment added** — a brief 1s segment was missed.
- **Start trim avg +200ms** — 400ms start padding was too much; ~200ms is the sweet spot.
- **End trim avg -100ms** — end padding was slightly tight; increased to ~200ms for safety.
- Final result: 8.5min from 24.4min raw (35% kept).

### Edit 2: 7min recording (12 → 19 segments)
- **0 segments removed** — content selection again 100% correct.
- **5 segments split** — segments of 33s, 18s, 14s, 35s, and even 5.8s were all split.
  User splits at ANY internal pause, not just long ones. Check every segment >5s.
- **1 micro-segment added** — user rescued "model system card" (1.3s) from a line
  discarded as a false start. When a false start contains useful context that the clean
  retake omits, extract that phrase as a micro-segment.
- **Stumble surgically removed** — user cut "struggles to solve like new and" by ending
  one segment before the stumble and starting the next after it. Don't keep stumbles/filler
  just because splitting feels awkward — the cut works better than the stumble.
- **Starts avg ~150ms later** — 200ms start padding is slightly generous.
- **Ends avg ~150ms earlier** — 200ms end padding is also slightly generous.
- **Prefer under-clipping** — user explicitly prefers too-long segments over clipped speech.
  Easier to trim excess in Premiere than to extend a clipped word.
- Final result: 2.5min from 7min raw (35% kept).

### Voice activity detection
Use VAD (voice activity detection) to verify segment boundaries. Transcript timestamps alone
can clip speech onset/offset. After determining segment boundaries from the transcript, use
VAD on the source audio to confirm that no speech is being clipped at the start or end of
each segment. If VAD detects speech energy at a segment boundary, extend the segment to
include it. This prevents the most common user correction: extending starts/ends where
speech was clipped.

## Transcription provider benchmark

See [BENCHMARK.md](BENCHMARK.md) for the full 4-way comparison (AssemblyAI, Deepgram, Azure, Google)
tested against 71 hand-corrected segments.

## Premiere Pro import

After generating the `.edl` file with `generate_edl.py`:

1. Open Premiere Pro
2. File > Import (Cmd+I / Ctrl+I)
3. Select the `.edl` file
4. When prompted, choose the matching frame rate (30fps for most screen recordings)
5. A new sequence appears in the Project panel
6. Right-click any offline clip > Link Media > navigate to the original MP4
7. All 58+ cuts are now on the timeline — scrub through to review and tweak

The EDL also works in DaVinci Resolve (File > Import Timeline > EDL) and most other NLEs.

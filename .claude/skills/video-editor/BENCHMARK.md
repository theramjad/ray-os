# Transcription Provider Benchmark

Tested 2026-02-23 on a 24.4min screen recording (single speaker, English).
Ground truth: 71 segments hand-corrected in Premiere Pro by the user.

| Metric | AssemblyAI | Deepgram | Azure | Google |
|---|---|---|---|---|
| Model | universal-3-pro | Nova-3 | Fast Transcription | latest_long (V1) |
| Word count | 3448 | 3430 | 3392 | 3442 |
| **Avg start distance** | **76ms** | 105ms | 150ms | 107ms |
| **Avg end distance** | 72ms | 165ms | **62ms** | 256ms |
| **Combined avg** | **74ms** | 135ms | 106ms | 181ms |
| Starts ≤100ms | 69.0% | 62.0% | 40.8% | **71.8%** |
| Starts ≤200ms | **93.0%** | 88.7% | 81.7% | 83.1% |
| Ends ≤100ms | 76.1% | 32.4% | **81.7%** | 9.9% |
| Ends ≤200ms | **97.2%** | 63.4% | **97.2%** | 35.2% |
| Max start error | **260ms** | 440ms | 993ms | 400ms |
| Max end error | 290ms | 350ms | **253ms** | 500ms |
| Start bias | +39ms | +58ms | +144ms | **+26ms** |
| Head-to-head wins | **41%** | 21% | 27% | 11% |

**Start distance** = how far the nearest word `start` timestamp is from the user's actual cut point.
**End distance** = how far the nearest word `end` timestamp is from the user's actual cut point.
**Start bias** = systematic offset (positive = word timestamps lag behind actual speech onset).
**Head-to-head** = % of 142 boundaries (71 starts + 71 ends) where provider was closest.

## Analysis

- **AssemblyAI wins overall**: best combined accuracy (74ms), best starts ≤200ms (93%), lowest
  combined distance. The clear choice for video editing.
- **Azure has the best end boundaries** (62ms avg) but the worst start bias (+144ms) and
  occasional large start errors (993ms max). Would need ~200ms more start padding than AssemblyAI.
- **Deepgram is weak on ends** (165ms avg, only 32% within 100ms). Starts are decent but
  still behind AssemblyAI.
- **Google has the lowest start bias** (+26ms) and best starts ≤100ms (71.8%), but **terrible
  end timestamps** (256ms avg, only 9.9% within 100ms). Requires FLAC input with explicit
  sample rate — MP3 input produced garbage (133 words of gibberish). Also requires GCS bucket
  for files >10MB, making it the most complex to set up.
- For video editing where tight start alignment matters most (clipping the beginning of speech
  is more noticeable than trailing ends), AssemblyAI's combination of low start distance (76ms)
  and low bias (+39ms) makes it the clear choice.

## Scripts

| Provider | Script | API key env var | Notes |
|---|---|---|---|
| AssemblyAI | `transcribe_assemblyai.py` | `ASSEMBLYAI_API_KEY` | Best overall |
| Deepgram | `transcribe_deepgram.py` | `DEEPGRAM_API_KEY` | |
| Azure | `transcribe_azure.py` | `AZURE_SPEECH_API_KEY` + `--region` | |
| Google | `transcribe_google.py` | `--credentials <sa.json>` + `--bucket` | Needs GCS + FLAC |

All scripts output the same AssemblyAI-compatible JSON format (`{words: [{text, start, end}]}`)
so format_transcript.py and the rest of the pipeline work with any provider.

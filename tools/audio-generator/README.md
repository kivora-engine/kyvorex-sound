# KYVOREX SOUNDS — Audio Generator

Small offline audio engine written in **pure Python** (standard library
only). It generates short WAV files by synthesis, and optionally
converts them to MP3 with FFmpeg.

No external sample. No downloaded loop. No third-party audio library.

## Modes

The generator has two modes:

| Mode | Command | Output |
|------|---------|--------|
| Test | `python generate.py` | `tools/audio-generator/output-test/` |
| Official | `python generate.py --official` | `<project>/audio/wav/` + `audio/mp3/` |

Test presets are for verification only. Official presets produce the
10 catalog sounds.

## Requirements

- Python 3.7 or newer.
- No NumPy, no SciPy, no librosa.
- FFmpeg is **optional** — only needed for MP3 conversion.

## Commands

### Generate test presets

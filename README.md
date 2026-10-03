# KYVOREX SOUNDS

Original sound library for game and app developers.

**Version 1.0** — 10 procedurally generated sounds.

## What's inside

- 10 sounds across Interface, Alerts, Gameplay and Sci-Fi
- Preview in the browser (procedural, Web Audio API)
- Download MP3 + WAV — real static files
- Static site — HTML, CSS, vanilla JavaScript, no backend

## Live site

https://kivora-engine.github.io/kyvorex-sound/

## Structure

    ├── index.html, sounds.html, about.html, license.html, 404.html
    ├── css/                  styles
    ├── js/                   frontend scripts
    ├── data/sounds.json      sound metadata
    ├── audio/wav, audio/mp3  the 10 sounds
    ├── tools/audio-generator Python engine (regenerates WAV/MP3)
    ├── scripts/build.js      production build → dist/
    └── .github/workflows/    build + deploy

## Audio formats

- WAV: mono, 44100 Hz, PCM 16-bit
- MP3: mono, 44100 Hz, LAME VBR

## Regenerating the audio (optional)

    cd tools/audio-generator
    python generate.py --official --sync-catalog

Requires Python 3.7+ and (for MP3) FFmpeg.

## Build

    npm install
    npm run build

The build writes to `dist/` and fails if any audio file is missing.

## License

This repository contains two distinct categories of content.

### Code
All rights reserved. No license granted for the source code.

### Sounds
Licensed under the **KYVOREX Free Sound License 1.0**.
- Free for personal and commercial use
- Free in games, apps, videos and other interactive works
- Attribution appreciated, not required
- Redistribution or resale as standalone files is not allowed
- May not be presented as your own original creations

Full text: [docs/LICENSE.txt](docs/LICENSE.txt) — [license.html](license.html)

### Brand
The KYVOREX name, the KYVOREX SOUNDS name and the logo are not covered
by either license.
"""KYVOREX SOUNDS - audio generator entry point.

Usage:
    python generate.py                              # test presets only
    python generate.py --official                   # all official sounds
    python generate.py --official --new-only        # only the latest new sounds
    python generate.py --official --sync-catalog    # + update sounds.json

Test presets go to tools/audio-generator/output-test/.
Official sounds go to <project>/audio/wav/ and audio/mp3/.

Catalog sources live in <project>/data/catalog/. `--sync-catalog`
updates their `status` field and then regenerates data/sounds.json.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
AUDIO_WAV = os.path.join(PROJECT_ROOT, 'audio', 'wav')
AUDIO_MP3 = os.path.join(PROJECT_ROOT, 'audio', 'mp3')
CATALOG_DIR = os.path.join(PROJECT_ROOT, 'data', 'catalog')
OUTPUT_TEST = os.path.join(HERE, 'output-test')


def _describe(samples, sr):
    n = len(samples)
    dur = n / float(sr) if sr else 0.0
    pk = max((abs(s) for s in samples), default=0.0)
    return "dur={0:.3f}s n={1} peak={2:.3f}".format(dur, n, pk)


def _file_info(path):
    if not os.path.isfile(path):
        return None
    size = os.path.getsize(path)
    return {'size': size, 'ok': size > 44}


# ---------------------------------------------------------------- tests

def run_tests():
    from presets import PRESETS
    from wav_export import write_wav
    from synthesis import DEFAULT_SAMPLE_RATE

    print("Mode       : test presets")
    print("Sample rate: {0} Hz".format(DEFAULT_SAMPLE_RATE))
    print("Output dir : {0}".format(OUTPUT_TEST))
    print("")

    os.makedirs(OUTPUT_TEST, exist_ok=True)
    print("Generating test sounds...")
    for name in sorted(PRESETS.keys()):
        samples = PRESETS[name]()
        path = os.path.join(OUTPUT_TEST, name + '.wav')
        write_wav(path, samples, DEFAULT_SAMPLE_RATE)
        print("Created: {0}".format(os.path.relpath(path, HERE)))
        print("         {0}".format(_describe(samples, DEFAULT_SAMPLE_RATE)))
    print("Done.")


# -------------------------------------------------------------- official

def _write_wavs(official_presets):
    from wav_export import write_wav
    from synthesis import DEFAULT_SAMPLE_RATE

    ok, failed = [], []
    print("Step 1/3: generating {0} official WAV files".format(len(official_presets)))
    print("         target: {0}".format(AUDIO_WAV))
    print("")

    for sid in sorted(official_presets.keys()):
        samples = official_presets[sid]()
        path = os.path.join(AUDIO_WAV, sid + '.wav')
        try:
            write_wav(path, samples, DEFAULT_SAMPLE_RATE)
            info = _file_info(path)
            if info and info['ok']:
                ok.append(sid)
                print("  WAV OK    {0:24s} {1}".format(sid, _describe(samples, DEFAULT_SAMPLE_RATE)))
            else:
                failed.append(sid)
                print("  WAV EMPTY {0}".format(sid))
        except Exception as e:
            failed.append(sid)
            print("  WAV ERROR {0}: {1}".format(sid, e))

    print("")
    return ok, failed


def _convert_mp3s(wav_ok):
    try:
        from mp3_convert import convert_to_mp3, has_ffmpeg
    except Exception:
        convert_to_mp3 = None
        has_ffmpeg = lambda: False

    if not has_ffmpeg():
        print("Step 2/3: MP3 conversion SKIPPED - FFmpeg not found on PATH.")
        print("         install FFmpeg, then re-run this command.")
        print("         on Termux:  pkg install ffmpeg")
        print("")
        return [], list(wav_ok), False

    print("Step 2/3: converting WAV -> MP3 with FFmpeg")
    print("         target: {0}".format(AUDIO_MP3))
    print("")

    ok, failed = [], []
    for sid in wav_ok:
        wav_path = os.path.join(AUDIO_WAV, sid + '.wav')
        mp3_path = os.path.join(AUDIO_MP3, sid + '.mp3')
        if convert_to_mp3(wav_path, mp3_path):
            info = _file_info(mp3_path)
            if info and info['size'] > 0:
                ok.append(sid)
                print("  MP3 OK    {0:24s} {1} bytes".format(sid, info['size']))
            else:
                failed.append(sid)
                print("  MP3 EMPTY {0}".format(sid))
        else:
            failed.append(sid)
            print("  MP3 FAIL  {0}   (ffmpeg exited with error)".format(sid))

    print("")
    return ok, failed, True


def _sync():
    print("Step 3/3: syncing catalog source files")
    print("         dir: {0}".format(CATALOG_DIR))
    print("")

    try:
        from catalog_sync import sync, rebuild_catalog
    except Exception as e:
        print("  catalog_sync import failed: {0}".format(e))
        return

    try:
        changed, summary = sync(CATALOG_DIR, AUDIO_WAV, AUDIO_MP3)
    except Exception as e:
        print("  catalog_sync failed: {0}".format(e))
        return

    for row in summary:
        print("  {0:24s} wav={1} mp3={2}  {3} -> {4}".format(
            row['id'],
            'y' if row['wav'] else 'n',
            'y' if row['mp3'] else 'n',
            row['old'], row['new']))
    print("")
    print("  Entries updated: {0}".format(changed))
    print("")

    print("Regenerating data/sounds.json from sources...")
    ok = rebuild_catalog(PROJECT_ROOT)
    if ok:
        print("  sounds.json regenerated.")
    else:
        print("  WARNING: sounds.json was NOT regenerated.")


def run_official(sync_catalog, new_only):
    from synthesis import DEFAULT_SAMPLE_RATE
    try:
        from mp3_convert import has_ffmpeg
    except Exception:
        has_ffmpeg = lambda: False

    presets_to_run = {}
    tag = "official"
    
    if new_only:
        # Mode new-only : ne génère que les derniers sons ajoutés (Science + Advanced UI)
        from official_presets_science import OFFICIAL_PRESETS_SCIENCE
        from official_presets_advanced_ui import OFFICIAL_PRESETS_ADV_UI
        presets_to_run = {**OFFICIAL_PRESETS_SCIENCE, **OFFICIAL_PRESETS_ADV_UI}
        tag = "new"
    else:
        # Mode complet : fusionne toutes les sources
        from official_presets import OFFICIAL_PRESETS
        from official_presets_extra import OFFICIAL_PRESETS_EXTRA
        from official_presets_quests import OFFICIAL_PRESETS_QUESTS
        from official_presets_music import OFFICIAL_PRESETS_MUSIC
        from official_presets_board import OFFICIAL_PRESETS_BOARD
        from official_presets_events import OFFICIAL_PRESETS_EVENTS
        from official_presets_science import OFFICIAL_PRESETS_SCIENCE
        from official_presets_advanced_ui import OFFICIAL_PRESETS_ADV_UI
        
        presets_to_run = {
            **OFFICIAL_PRESETS, 
            **OFFICIAL_PRESETS_EXTRA, 
            **OFFICIAL_PRESETS_QUESTS,
            **OFFICIAL_PRESETS_MUSIC,
            **OFFICIAL_PRESETS_BOARD,
            **OFFICIAL_PRESETS_EVENTS,
            **OFFICIAL_PRESETS_SCIENCE,
            **OFFICIAL_PRESETS_ADV_UI
        }
        tag = "all"

    total = len(presets_to_run)
    print("Mode        : official catalog ({0})".format(tag))
    print("Sample rate : {0} Hz".format(DEFAULT_SAMPLE_RATE))
    print("FFmpeg      : {0}".format('yes' if has_ffmpeg() else 'no'))
    print("")

    os.makedirs(AUDIO_WAV, exist_ok=True)
    os.makedirs(AUDIO_MP3, exist_ok=True)

    wav_ok, wav_failed = _write_wavs(presets_to_run)
    mp3_ok, mp3_failed, ffmpeg_present = _convert_mp3s(wav_ok)

    if sync_catalog:
        _sync()

    print("")
    print("=========================================")
    print("FINAL REPORT")
    print("=========================================")
    print("  WAV : {0}/{1} OK   ({2} failed)".format(len(wav_ok), total, len(wav_failed)))
    print("  MP3 : {0}/{1} OK   ({2} failed)".format(len(mp3_ok), total, len(mp3_failed)))
    if not ffmpeg_present:
        print("  NOTE: FFmpeg was not available. MP3 files were not produced.")
        print("        Install FFmpeg and re-run with --official.")
    print("")

    if wav_failed:
        print("  WAV failed  : {0}".format(', '.join(wav_failed)))
    if mp3_failed and ffmpeg_present:
        print("  MP3 failed  : {0}".format(', '.join(mp3_failed)))
    print("")

    if len(wav_ok) == total and len(mp3_ok) == total:
        print("  STATUS: COMPLETE - all {0} WAV and {0} MP3 files are ready.".format(total))
        return 0

    if len(wav_ok) == total and not ffmpeg_present:
        print("  STATUS: WAV COMPLETE, MP3 MISSING - FFmpeg required.")
        return 0

    if wav_failed:
        print("  STATUS: INCOMPLETE - WAV generation failed for some IDs.")
        return 1

    print("  STATUS: WAV COMPLETE, MP3 INCOMPLETE.")
    return 1


# ---------------------------------------------------------------- entry

def main():
    parser = argparse.ArgumentParser(
        description='KYVOREX SOUNDS - procedural audio generator'
    )
    parser.add_argument('--official', action='store_true',
                        help='Generate the official catalog sounds')
    parser.add_argument('--new-only', action='store_true',
                        help='Generate only the latest new sounds (Science + Advanced UI)')
    parser.add_argument('--sync-catalog', action='store_true',
                        help='Update catalog source status and regenerate sounds.json')
    args = parser.parse_args()

    print("KYVOREX SOUNDS - Audio Generator")
    print("")

    if args.official:
        code = run_official(sync_catalog=args.sync_catalog, new_only=args.new_only)
        sys.exit(code)
    else:
        if args.sync_catalog:
            print("Note: --sync-catalog is ignored without --official.")
            print("")
        run_tests()


if __name__ == '__main__':
    main()
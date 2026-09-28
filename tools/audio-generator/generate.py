"""KYVOREX SOUNDS - audio generator entry point.

Usage:
    python generate.py                              # test presets only
    python generate.py --official                   # 10 official sounds
    python generate.py --official --sync-catalog    # + update sounds.json

Test presets go to tools/audio-generator/output-test/.
Official sounds go to <project>/audio/wav/ and audio/mp3/.
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
OUTPUT_TEST = os.path.join(HERE, 'output-test')
SOUNDS_JSON = os.path.join(PROJECT_ROOT, 'data', 'sounds.json')


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
    """Returns (ok_ids, failed_ids)."""
    from wav_export import write_wav
    from synthesis import DEFAULT_SAMPLE_RATE

    ok, failed = [], []
    print("Step 1/3: generating 10 official WAV files")
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
    """Returns (ok_ids, failed_ids, ffmpeg_present)."""
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


def _sync(json_path):
    print("Step 3/3: syncing data/sounds.json")
    print("         file: {0}".format(json_path))
    print("")
    try:
        from catalog_sync import sync
    except Exception as e:
        print("  catalog_sync import failed: {0}".format(e))
        return

    try:
        changed, summary = sync(json_path, AUDIO_WAV, AUDIO_MP3)
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


def run_official(sync_catalog):
    from official_presets import OFFICIAL_PRESETS
    from synthesis import DEFAULT_SAMPLE_RATE

    try:
        from mp3_convert import has_ffmpeg
    except Exception:
        has_ffmpeg = lambda: False

    total = len(OFFICIAL_PRESETS)

    print("Mode        : official catalog")
    print("Sample rate : {0} Hz".format(DEFAULT_SAMPLE_RATE))
    print("WAV dir     : {0}".format(AUDIO_WAV))
    print("MP3 dir     : {0}".format(AUDIO_MP3))
    print("FFmpeg      : {0}".format('yes' if has_ffmpeg() else 'no'))
    print("")

    os.makedirs(AUDIO_WAV, exist_ok=True)
    os.makedirs(AUDIO_MP3, exist_ok=True)

    wav_ok, wav_failed = _write_wavs(OFFICIAL_PRESETS)
    mp3_ok, mp3_failed, ffmpeg_present = _convert_mp3s(wav_ok)

    if sync_catalog:
        _sync(SOUNDS_JSON)

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
                        help='Generate the 10 official catalog sounds')
    parser.add_argument('--sync-catalog', action='store_true',
                        help='Update data/sounds.json status (only with --official)')
    args = parser.parse_args()

    print("KYVOREX SOUNDS - Audio Generator")
    print("")

    if args.official:
        code = run_official(sync_catalog=args.sync_catalog)
        sys.exit(code)
    else:
        if args.sync_catalog:
            print("Note: --sync-catalog is ignored without --official.")
            print("")
        run_tests()


if __name__ == '__main__':
    main()
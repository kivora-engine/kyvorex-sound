import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
AUDIO_WAV = os.path.join(PROJECT_ROOT, 'audio', 'wav')
AUDIO_MP3 = os.path.join(PROJECT_ROOT, 'audio', 'mp3')
CATALOG_DIR = os.path.join(PROJECT_ROOT, 'data', 'catalog')
OUTPUT_TEST = os.path.join(HERE, 'output-test')

def _describe(samples, sr):
    n = len(samples); dur = n / float(sr) if sr else 0.0
    pk = max((abs(s) for s in samples), default=0.0)
    return "dur={0:.3f}s n={1} peak={2:.3f}".format(dur, n, pk)

def _file_info(path):
    if not os.path.isfile(path): return None
    size = os.path.getsize(path)
    return {'size': size, 'ok': size > 44}

def run_tests():
    from presets import PRESETS
    from wav_export import write_wav
    from synthesis import DEFAULT_SAMPLE_RATE
    print("Mode       : test presets")
    os.makedirs(OUTPUT_TEST, exist_ok=True)
    for name in sorted(PRESETS.keys()):
        samples = PRESETS[name]()
        path = os.path.join(OUTPUT_TEST, name + '.wav')
        write_wav(path, samples, DEFAULT_SAMPLE_RATE)
        print("Created: {0}".format(os.path.relpath(path, HERE)))
    print("Done.")

def _write_wavs(presets_to_run, tag="official"):
    from wav_export import write_wav
    from synthesis import DEFAULT_SAMPLE_RATE
    ok, failed = [], []
    print("Step 1/3: generating {0} {1} WAV files".format(len(presets_to_run), tag))
    for sid in sorted(presets_to_run.keys()):
        samples = presets_to_run[sid]()
        path = os.path.join(AUDIO_WAV, sid + '.wav')
        try:
            write_wav(path, samples, DEFAULT_SAMPLE_RATE)
            info = _file_info(path)
            if info and info['ok']: ok.append(sid)
            else: failed.append(sid)
        except Exception as e: failed.append(sid)
    print("  WAV OK: {0}, Failed: {1}".format(len(ok), len(failed)))
    return ok, failed

def _convert_mp3s(wav_ok):
    try:
        from mp3_convert import convert_to_mp3, has_ffmpeg
    except Exception:
        convert_to_mp3 = None; has_ffmpeg = lambda: False
    if not has_ffmpeg():
        print("Step 2/3: MP3 conversion SKIPPED - FFmpeg not found.")
        return [], list(wav_ok), False
    ok, failed = [], []
    print("Step 2/3: converting WAV -> MP3 with FFmpeg")
    for sid in wav_ok:
        wav_path = os.path.join(AUDIO_WAV, sid + '.wav')
        mp3_path = os.path.join(AUDIO_MP3, sid + '.mp3')
        if convert_to_mp3(wav_path, mp3_path): ok.append(sid)
        else: failed.append(sid)
    print("  MP3 OK: {0}, Failed: {1}".format(len(ok), len(failed)))
    return ok, failed, True

def _sync():
    print("Step 3/3: syncing catalog source files")
    try:
        from catalog_sync import sync, rebuild_catalog
        changed, summary = sync(CATALOG_DIR, AUDIO_WAV, AUDIO_MP3)
        print("  Entries updated: {0}".format(changed))
        rebuild_catalog(PROJECT_ROOT)
    except Exception as e:
        print("  catalog_sync failed: {0}".format(e))

def run_official(sync_catalog, new_only):
    from synthesis import DEFAULT_SAMPLE_RATE
    try:
        from mp3_convert import has_ffmpeg
    except Exception:
        has_ffmpeg = lambda: False

    presets_to_run = {}
    tag = "official"
    
    if new_only:
        from official_presets_extra import OFFICIAL_PRESETS_EXTRA
        presets_to_run = OFFICIAL_PRESETS_EXTRA
        tag = "new"
    else:
        from official_presets import OFFICIAL_PRESETS
        from official_presets_extra import OFFICIAL_PRESETS_EXTRA
        presets_to_run = {**OFFICIAL_PRESETS, **OFFICIAL_PRESETS_EXTRA}
        tag = "all"

    total = len(presets_to_run)
    print("Mode        : official catalog ({0})".format(tag))
    print("Sample rate : {0} Hz".format(DEFAULT_SAMPLE_RATE))
    print("FFmpeg      : {0}".format('yes' if has_ffmpeg() else 'no'))
    print("")

    os.makedirs(AUDIO_WAV, exist_ok=True)
    os.makedirs(AUDIO_MP3, exist_ok=True)

    wav_ok, wav_failed = _write_wavs(presets_to_run, tag)
    mp3_ok, mp3_failed, ffmpeg_present = _convert_mp3s(wav_ok)

    if sync_catalog: _sync()

    print("")
    print("FINAL REPORT")
    print("  WAV : {0}/{1} OK".format(len(wav_ok), total))
    print("  MP3 : {0}/{1} OK".format(len(mp3_ok), total))
    if wav_failed: print("  WAV failed  : {0}".format(', '.join(wav_failed)))
    if mp3_failed and ffmpeg_present: print("  MP3 failed  : {0}".format(', '.join(mp3_failed)))
    
    if len(wav_ok) == total and len(mp3_ok) == total:
        print("  STATUS: COMPLETE")
        return 0
    if len(wav_ok) == total and not ffmpeg_present:
        print("  STATUS: WAV COMPLETE, MP3 MISSING - FFmpeg required.")
        return 0
    print("  STATUS: INCOMPLETE.")
    return 1

def main():
    parser = argparse.ArgumentParser(description='KYVOREX SOUNDS - procedural audio generator')
    parser.add_argument('--official', action='store_true', help='Generate official catalog sounds')
    parser.add_argument('--new-only', action='store_true', help='Generate only the extra 30 new sounds')
    parser.add_argument('--sync-catalog', action='store_true', help='Update catalog status and rebuild sounds.json')
    args = parser.parse_args()

    print("KYVOREX SOUNDS - Audio Generator\n")
    if args.official:
        code = run_official(sync_catalog=args.sync_catalog, new_only=args.new_only)
        sys.exit(code)
    else:
        if args.sync_catalog: print("Note: --sync-catalog is ignored without --official.")
        run_tests()

if __name__ == '__main__':
    main()
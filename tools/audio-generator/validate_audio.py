"""Post-generation validation: open WAV files, check format, duration."""
import os
import wave


def check_wav(path):
    if not os.path.isfile(path):
        return {"ok": False, "error": "missing"}
    try:
        with wave.open(path, "rb") as wf:
            nch = wf.getnchannels()
            sr = wf.getframerate()
            sw = wf.getsampwidth()
            n = wf.getnframes()
            data = wf.readframes(n)
        if not data:
            return {"ok": False, "error": "empty"}
        dur = n / float(sr) if sr else 0.0
        return {
            "ok": True,
            "channels": nch,
            "sample_rate": sr,
            "sample_width": sw,
            "frames": n,
            "duration": dur,
            "bytes": len(data),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def validate_set(items, base_dir):
    """items: list of (name, min_dur, max_dur). Returns list of results."""
    results = []
    for name, dmin, dmax in items:
        path = os.path.join(base_dir, name + ".wav")
        info = check_wav(path)
        info["name"] = name
        info["expected"] = (dmin, dmax)
        if info.get("ok"):
            d = info["duration"]
            info["duration_ok"] = (dmin <= d <= dmax)
            info["format_ok"] = (
                info["channels"] == 1
                and info["sample_rate"] == 44100
                and info["sample_width"] == 2
            )
        results.append(info)
    return results


def summarize(results):
    total = len(results)
    ok_count = sum(1 for r in results if r.get("ok"))
    format_ok = sum(1 for r in results if r.get("format_ok"))
    duration_ok = sum(1 for r in results if r.get("duration_ok"))
    return {
        "total": total,
        "present": ok_count,
        "format_ok": format_ok,
        "duration_ok": duration_ok,
    }
"""FFmpeg wrapper for MP3 conversion. Optional - WAV generation does
not depend on FFmpeg."""
import os
import shutil
import subprocess


def has_ffmpeg():
    return shutil.which('ffmpeg') is not None


def convert_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 with FFmpeg. Returns True on success."""
    if not has_ffmpeg():
        return False
    if not os.path.isfile(wav_path):
        return False

    parent = os.path.dirname(mp3_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', wav_path,
        '-codec:a', 'libmp3lame',
        '-qscale:a', '2',
        mp3_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except Exception:
        return False
    return os.path.isfile(mp3_path) and os.path.getsize(mp3_path) > 0
#!/usr/bin/env python3
"""Split recordings containing discrete bird sounds separated by silence.

Requires Python, numpy, soundfile, and FFmpeg for MP3 output.
Example:
    python soundborb_split.py "Beep Boop.wav" --output review

The original is read-only. Splits are based on audio samples, not manual guesses.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
import soundfile as sf


def split_audio(source: Path, output: Path, threshold=1e-5, min_silence_ms=150,
                min_event_ms=80, pad_before_ms=100, pad_after_ms=150):
    samples, sr = sf.read(source, dtype='float64', always_2d=True)
    sample_count = len(samples)
    if not sample_count:
        raise ValueError('Empty audio file')
    active = np.flatnonzero(np.max(np.abs(samples), axis=1) > threshold)
    if not len(active):
        raise ValueError('No audio regions above threshold')

    breaks = np.flatnonzero(np.diff(active) > round(min_silence_ms * sr / 1000))
    starts = np.concatenate(([active[0]], active[breaks + 1]))
    ends = np.concatenate((active[breaks] + 1, [active[-1] + 1]))  # exclusive
    events = [(int(a), int(b)) for a, b in zip(starts, ends)
              if (b-a) >= round(min_event_ms*sr/1000)]
    if not events:
        raise ValueError('No events long enough to export')

    output.mkdir(parents=True, exist_ok=True)
    mp3_dir = output/'mp3'
    wav_dir = output/'wav'
    mp3_dir.mkdir(exist_ok=True)
    wav_dir.mkdir(exist_ok=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    safe_stem = ''.join(c.lower() if c.isalnum() else '-' for c in source.stem).strip('-')
    rows = []
    for i, (start, end) in enumerate(events, 1):
        begin = max(0, start - round(sr*pad_before_ms/1000))
        finish = min(sample_count, end + round(sr*pad_after_ms/1000))
        # Avoid overlapping with neighbouring event, if needed.
        if i > 1:
            begin = max(begin, (events[i-2][1] + start)//2)
        if i < len(events):
            finish = min(finish, (end + events[i][0])//2)
        label = f'{safe_stem}-{i:03d}'
        wav_path = wav_dir/f'{label}.wav'
        mp3_path = mp3_dir/f'{label}.mp3'
        clip = samples[begin:finish]
        sf.write(wav_path, clip, sr, subtype='PCM_24')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav_path),
               '-vn', '-codec:a', 'libmp3lame', '-b:a', '192k', str(mp3_path)]
        subprocess.run(cmd, check=True)
        # 48 small waveform peak buckets, no audio bytes embedded in metadata.
        mono = clip.mean(axis=1)
        buckets = [float(np.max(np.abs(part))) if len(part) else 0.0
                   for part in np.array_split(mono, 48)]
        rows.append({
            'id': label, 'name': f'Sound {i:02d}',
            'source_file': source.name, 'source_sha256': digest,
            'event_start_seconds': round(start/sr, 6),
            'event_end_seconds': round(end/sr, 6),
            'clip_start_seconds': round(begin/sr, 6),
            'clip_end_seconds': round(finish/sr, 6),
            'clip_duration_seconds': round((finish-begin)/sr, 6),
            'mp3': f'mp3/{label}.mp3', 'wav': f'wav/{label}.wav',
            'peak': round(float(np.max(np.abs(clip))), 6),
            'waveform': buckets
        })
    info = {
        'title': source.name, 'source_sha256': digest,
        'source_duration_seconds': round(sample_count/sr, 6),
        'sample_rate': sr, 'channels': samples.shape[1],
        'parameters': {
            'absolute_sample_threshold': threshold,
            'minimum_silence_ms': min_silence_ms,
            'minimum_event_ms': min_event_ms,
            'pad_before_ms': pad_before_ms,
            'pad_after_ms': pad_after_ms,
            'normalization': 'none', 'noise_reduction': 'none',
            'mp3_bitrate_kbps': 192,
        },
        'clips': rows,
    }
    (output/'manifest.json').write_text(json.dumps(info, indent=2), encoding='utf-8')
    with (output/'manifest.csv').open('w', newline='', encoding='utf-8') as f:
        keys = [k for k in rows[0].keys() if k != 'waveform']
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows({k: row[k] for k in keys} for row in rows)
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, default=Path('soundborb_review'))
    parser.add_argument('--threshold', type=float, default=1e-5)
    parser.add_argument('--min-silence-ms', type=float, default=150)
    parser.add_argument('--min-event-ms', type=float, default=80)
    parser.add_argument('--pad-before-ms', type=float, default=100)
    parser.add_argument('--pad-after-ms', type=float, default=150)
    args = parser.parse_args()
    info = split_audio(args.source, args.output, args.threshold, args.min_silence_ms,
                       args.min_event_ms, args.pad_before_ms, args.pad_after_ms)
    print(f"Generated {len(info['clips'])} clips in {args.output}")

if __name__ == '__main__':
    main()
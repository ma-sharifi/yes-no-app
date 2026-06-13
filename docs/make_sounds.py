#!/usr/bin/env python3
"""Generate the two short tap sounds bundled with the app.

- yes.wav: a bright, ascending three-note chime (affirmative).
- no.wav:  a lower, descending two-note tone (negative).

16-bit mono PCM WAV, generated with the stdlib only so the build host needs
no audio libraries. The files live in YesNo/ and are picked up automatically
by the file-system synchronized group as bundle resources.
"""
import math
import struct
import wave

RATE = 44100
AMP = 0.55


def tone(freq, dur, sample_index_start=0):
    """A single sine tone with a short attack/decay envelope (no clicks)."""
    n = int(RATE * dur)
    out = []
    attack = int(0.01 * RATE)
    release = int(0.06 * RATE)
    for i in range(n):
        if i < attack:
            env = i / attack
        elif i > n - release:
            env = max(0.0, (n - i) / release)
        else:
            env = 1.0
        out.append(AMP * env * math.sin(2 * math.pi * freq * i / RATE))
    return out


def write_wav(path, notes):
    """notes: list of (freq, duration) played in sequence."""
    samples = []
    for freq, dur in notes:
        samples.extend(tone(freq, dur))
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        frames = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767))
                           for s in samples)
        w.writeframes(frames)
    print("wrote", path, f"({len(samples) / RATE:.2f}s)")


# Yes: C5 -> E5 -> G5 ascending major arpeggio.
write_wav("YesNo/yes.wav", [(523.25, 0.08), (659.25, 0.08), (783.99, 0.16)])

# No: A4 -> F4 descending.
write_wav("YesNo/no.wav", [(440.00, 0.10), (349.23, 0.20)])

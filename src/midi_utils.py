"""
MIDI utility functions for YM2151 conversion.
Handles MIDI note to YM2151 KC/KF conversion.
"""


def midi_to_kc_kf(midi_note):
    """
    Convert MIDI note to YM2151 KC (Key Code) and KF (Key Fraction).

    Args:
        midi_note: MIDI note number (0-127)

    Returns:
        tuple: (kc, kf) where kc is the key code and kf is the key fraction
    """
    # YM2151 note table (based on ym2151-zig-cc implementation)
    note_table = [
        0,  # C#
        1,  # D
        2,  # D#
        4,  # E
        5,  # F
        6,  # F#
        8,  # G
        9,  # G#
        10,  # A
        12,  # A#
        13,  # B
        14,  # C
    ]

    # Adjust MIDI note by -1 to align octaves (prevent underflow)
    adjusted_midi = midi_note - 1 if midi_note > 0 else 0
    midi_octave = (adjusted_midi // 12) - 1

    # Clamp octave to valid range (0-7 for YM2151)
    midi_octave = max(0, min(7, midi_octave))

    note_in_octave = adjusted_midi % 12
    ym_note = note_table[note_in_octave]

    kc = (midi_octave << 4) | ym_note
    kf = 0  # No fine tuning for now

    return kc, kf


def ticks_to_seconds(ticks, ticks_per_beat, tempo_bpm):
    """
    Convert MIDI ticks to seconds.

    Args:
        ticks: Number of MIDI ticks
        ticks_per_beat: Ticks per quarter note (from MIDI file)
        tempo_bpm: Tempo in beats per minute

    Returns:
        float: Time in seconds
    """
    seconds_per_beat = 60.0 / tempo_bpm
    seconds_per_tick = seconds_per_beat / ticks_per_beat
    return ticks * seconds_per_tick


def seconds_to_samples(seconds, sample_rate=55930):
    """
    Convert seconds to sample count.

    Args:
        seconds: Time in seconds
        sample_rate: Sample rate (default: 55930 Hz for YM2151)

    Returns:
        int: Sample count
    """
    return int(seconds * sample_rate)


def ticks_to_samples(ticks, ticks_per_beat, tempo_bpm, sample_rate=55930):
    """
    Convert MIDI ticks directly to sample count.

    Args:
        ticks: Number of MIDI ticks
        ticks_per_beat: Ticks per quarter note
        tempo_bpm: Tempo in beats per minute
        sample_rate: Sample rate (default: 55930 Hz for YM2151)

    Returns:
        int: Sample count
    """
    seconds = ticks_to_seconds(ticks, ticks_per_beat, tempo_bpm)
    return seconds_to_samples(seconds, sample_rate)

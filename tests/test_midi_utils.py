"""Unit tests for MIDI utility functions."""

from src.midi_utils import midi_to_kc_kf, seconds_to_samples, ticks_to_samples, ticks_to_seconds


def test_midi_to_kc_kf_middle_c():
    """Test MIDI note 60 (C4) conversion."""
    kc, kf = midi_to_kc_kf(60)
    assert kf == 0
    assert isinstance(kc, int)


def test_midi_to_kc_kf_a4():
    """Test MIDI note 69 (A4, 440Hz) conversion."""
    kc, kf = midi_to_kc_kf(69)
    # Should match YM2151's A4 (KC 0x4A from reference)
    assert kc == 0x4A
    assert kf == 0


def test_midi_to_kc_kf_boundary():
    """Test boundary cases for MIDI note conversion."""
    # Test note 0
    kc, kf = midi_to_kc_kf(0)
    assert isinstance(kc, int)
    assert kf == 0

    # Test note 127 (max MIDI note)
    kc, kf = midi_to_kc_kf(127)
    assert isinstance(kc, int)
    assert kf == 0


def test_ticks_to_seconds():
    """Test MIDI ticks to seconds conversion."""
    # At 120 BPM, 480 ticks per beat
    # 480 ticks should be 0.5 seconds (one quarter note)
    seconds = ticks_to_seconds(480, 480, 120)
    assert abs(seconds - 0.5) < 0.001


def test_seconds_to_samples():
    """Test seconds to samples conversion."""
    # 1 second at 55930 Hz should be 55930 samples
    samples = seconds_to_samples(1.0, 55930)
    assert samples == 55930

    # 0.5 seconds should be 27965 samples
    samples = seconds_to_samples(0.5, 55930)
    assert samples == 27965


def test_ticks_to_samples():
    """Test direct MIDI ticks to samples conversion."""
    # At 120 BPM, 480 ticks per beat, 55930 Hz
    # 480 ticks (quarter note) = 0.5 seconds = 27965 samples
    samples = ticks_to_samples(480, 480, 120, 55930)
    assert samples == 27965

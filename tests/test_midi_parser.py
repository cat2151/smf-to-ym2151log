"""Unit tests for MIDI parser."""

import pytest
import mido
import tempfile
import os
from src.midi_parser import parse_midi_file


def test_parse_simple_midi():
    """Test parsing a simple MIDI file."""
    # Create a temporary MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    track.append(mido.Message('note_on', note=60, velocity=100, time=0))
    track.append(mido.Message('note_off', note=60, velocity=0, time=480))
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mid', delete=False) as f:
        mid.save(file=f)
        temp_path = f.name
    
    try:
        # Parse the file
        result = parse_midi_file(temp_path)
        
        # Verify structure
        assert 'ticks_per_beat' in result
        assert 'tempo_bpm' in result
        assert 'events' in result
        
        # Check events
        assert len(result['events']) >= 2
        
        # Find note events
        note_on_events = [e for e in result['events'] if e['type'] == 'note_on']
        note_off_events = [e for e in result['events'] if e['type'] == 'note_off']
        
        assert len(note_on_events) == 1
        assert len(note_off_events) == 1
        assert note_on_events[0]['note'] == 60
        
    finally:
        # Clean up
        os.unlink(temp_path)


def test_parse_tempo_changes():
    """Test parsing MIDI file with tempo changes."""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add tempo changes
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120), time=0))
    track.append(mido.Message('note_on', note=60, velocity=100, time=0))
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(140), time=480))
    track.append(mido.Message('note_off', note=60, velocity=0, time=0))
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mid', delete=False) as f:
        mid.save(file=f)
        temp_path = f.name
    
    try:
        result = parse_midi_file(temp_path)
        
        # Find tempo events
        tempo_events = [e for e in result['events'] if e['type'] == 'tempo']
        assert len(tempo_events) >= 2
        
    finally:
        os.unlink(temp_path)

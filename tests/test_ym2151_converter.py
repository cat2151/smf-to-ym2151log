"""Unit tests for YM2151 converter."""

import pytest
from src.ym2151_init import initialize_channel_events
from src.ym2151_converter import convert_to_ym2151_log


def test_initialize_channel_events():
    """Test channel initialization generates correct events."""
    events = initialize_channel_events(0, 0)
    
    # Should have multiple events for initialization
    assert len(events) > 0
    
    # All events should have required fields
    for event in events:
        assert 'time' in event
        assert 'addr' in event
        assert 'data' in event
        assert 'is_data' in event
        
    # Check time is correct
    assert all(event['time'] == 0 for event in events)
    
    # Check format of addr and data
    for event in events:
        assert event['addr'].startswith('0x')
        assert event['data'].startswith('0x')


def test_convert_to_ym2151_log_structure():
    """Test YM2151 log output structure."""
    midi_data = {
        'ticks_per_beat': 480,
        'tempo_bpm': 120,
        'events': []
    }
    
    result = convert_to_ym2151_log(midi_data)
    
    # Check structure
    assert 'event_count' in result
    assert 'events' in result
    assert isinstance(result['events'], list)
    assert result['event_count'] == len(result['events'])


def test_convert_to_ym2151_log_with_notes():
    """Test YM2151 log generation with note events."""
    midi_data = {
        'ticks_per_beat': 480,
        'tempo_bpm': 120,
        'events': [
            {'type': 'note_on', 'ticks': 0, 'channel': 0, 'note': 60, 'velocity': 100},
            {'type': 'note_off', 'ticks': 480, 'channel': 0, 'note': 60}
        ]
    }
    
    result = convert_to_ym2151_log(midi_data)
    
    # Should have initialization + note events
    assert result['event_count'] > 0
    assert len(result['events']) > 0
    
    # All events should have proper format
    for event in result['events']:
        assert 'time' in event
        assert 'addr' in event
        assert 'data' in event
        assert 'is_data' in event
        assert event['addr'].startswith('0x')
        assert event['data'].startswith('0x')
        assert isinstance(event['time'], int)
        assert isinstance(event['is_data'], int)

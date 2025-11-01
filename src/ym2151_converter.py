"""
YM2151 converter module - Pass B: Convert events to YM2151 log JSON.
Generates YM2151 register write events in the format expected by ym2151-zig-cc.
"""

from src.midi_utils import midi_to_kc_kf, ticks_to_samples
from src.ym2151_init import initialize_channel_events


def convert_to_ym2151_log(midi_events_data):
    """
    Convert parsed MIDI events to YM2151 register write events.
    
    Args:
        midi_events_data: Parsed MIDI data from midi_parser
        
    Returns:
        dict: YM2151 log with event_count and events list
    """
    ticks_per_beat = midi_events_data['ticks_per_beat']
    tempo_bpm = midi_events_data['tempo_bpm']
    midi_events = midi_events_data['events']
    
    ym2151_events = []
    
    # Initialize all channels at time 0
    for ch in range(8):
        ym2151_events.append({
            'time': 0,
            'addr': '0x08',
            'data': f'0x{ch:02X}',
            'is_data': 0
        })
    
    # Initialize channel 0 with default parameters
    ym2151_events.extend(initialize_channel_events(0, 0))
    
    # Process MIDI events
    active_notes = {}  # Track active notes per channel
    
    for event in midi_events:
        if event['type'] == 'note_on':
            sample_time = ticks_to_samples(
                event['ticks'],
                ticks_per_beat,
                tempo_bpm
            )
            
            channel = 0  # Use channel 0 for now (mono)
            note = event['note']
            kc, kf = midi_to_kc_kf(note)
            
            # Set KC (Key Code)
            ym2151_events.append({
                'time': sample_time,
                'addr': f'0x{0x28 + channel:02X}',
                'data': f'0x{kc:02X}',
                'is_data': 0
            })
            
            # Set KF (Key Fraction)
            ym2151_events.append({
                'time': sample_time,
                'addr': f'0x{0x30 + channel:02X}',
                'data': f'0x{kf:02X}',
                'is_data': 0
            })
            
            # Key ON
            ym2151_events.append({
                'time': sample_time,
                'addr': '0x08',
                'data': f'0x{0x78 | channel:02X}',
                'is_data': 0
            })
            
            active_notes[(event['channel'], note)] = True
            
        elif event['type'] == 'note_off':
            sample_time = ticks_to_samples(
                event['ticks'],
                ticks_per_beat,
                tempo_bpm
            )
            
            channel = 0  # Use channel 0 for now (mono)
            note = event['note']
            
            if (event['channel'], note) in active_notes:
                # Key OFF
                ym2151_events.append({
                    'time': sample_time,
                    'addr': '0x08',
                    'data': f'0x{channel:02X}',
                    'is_data': 0
                })
                
                del active_notes[(event['channel'], note)]
    
    return {
        'event_count': len(ym2151_events),
        'events': ym2151_events
    }

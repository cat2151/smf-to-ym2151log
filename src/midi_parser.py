"""
MIDI parser module - Pass A: Convert MIDI file to events JSON.
Extracts MIDI events and converts them to an intermediate format.
"""

import mido


def parse_midi_file(midi_filename):
    """
    Parse a Standard MIDI File and extract relevant events.
    
    Args:
        midi_filename: Path to MIDI file
        
    Returns:
        dict: Parsed MIDI data with events list and metadata
    """
    mid = mido.MidiFile(midi_filename)
    
    events = []
    absolute_time = 0
    tempo_bpm = 120  # Default tempo
    
    # Get ticks per beat from MIDI file
    ticks_per_beat = mid.ticks_per_beat
    
    # Process all tracks
    for i, track in enumerate(mid.tracks):
        absolute_time = 0
        
        for msg in track:
            absolute_time += msg.time
            
            # Extract tempo changes
            if msg.type == 'set_tempo':
                # Convert microseconds per beat to BPM
                tempo_bpm = mido.tempo2bpm(msg.tempo)
                events.append({
                    'type': 'tempo',
                    'ticks': absolute_time,
                    'tempo_bpm': tempo_bpm
                })
            
            # Extract note on events
            elif msg.type == 'note_on' and msg.velocity > 0:
                events.append({
                    'type': 'note_on',
                    'ticks': absolute_time,
                    'channel': msg.channel,
                    'note': msg.note,
                    'velocity': msg.velocity
                })
            
            # Extract note off events (including note_on with velocity 0)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                events.append({
                    'type': 'note_off',
                    'ticks': absolute_time,
                    'channel': msg.channel,
                    'note': msg.note
                })
            
            # Extract program change events
            elif msg.type == 'program_change':
                events.append({
                    'type': 'program_change',
                    'ticks': absolute_time,
                    'channel': msg.channel,
                    'program': msg.program
                })
    
    return {
        'ticks_per_beat': ticks_per_beat,
        'tempo_bpm': tempo_bpm,
        'events': events
    }

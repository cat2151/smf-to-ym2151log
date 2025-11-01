#!/usr/bin/env python3
"""
Create a simple test MIDI file for testing the converter.
Generates a simple melody: C4, E4, G4, B4
"""

import mido


def create_test_midi():
    """Create a simple test MIDI file."""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo to 120 BPM
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    
    # Ticks per beat
    mid.ticks_per_beat = 480
    
    # Play notes C4 (60), E4 (64), G4 (67), B4 (71)
    notes = [60, 64, 67, 71]
    
    for note in notes:
        # Note on
        track.append(mido.Message('note_on', note=note, velocity=100, time=0))
        # Note off after quarter note (480 ticks)
        track.append(mido.Message('note_off', note=note, velocity=0, time=480))
    
    # Save to file
    mid.save('test.mid')
    print("Created test.mid with notes: C4, E4, G4, B4")


if __name__ == '__main__':
    create_test_midi()

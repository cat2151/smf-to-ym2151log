#!/usr/bin/env python3
"""
SMF to YM2151 Log Converter
Converts Standard MIDI Files to YM2151 register write log in JSON format.

Usage:
    python smf_to_ym2151log.py <midi_file>
"""

import sys
import json
import os
from src.midi_parser import parse_midi_file
from src.ym2151_converter import convert_to_ym2151_log


def main():
    """Main entry point for the converter."""
    if len(sys.argv) < 2:
        print("Usage: python smf_to_ym2151log.py <midi_file>")
        print("  <midi_file>: Path to Standard MIDI File")
        sys.exit(1)
    
    midi_filename = sys.argv[1]
    
    if not os.path.exists(midi_filename):
        print(f"Error: File '{midi_filename}' not found")
        sys.exit(1)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(midi_filename))[0]
    
    print(f"Processing: {midi_filename}")
    
    # Pass A: Parse MIDI file to events JSON
    print("\nPass A: Parsing MIDI file...")
    midi_events_data = parse_midi_file(midi_filename)
    
    # Save Pass A output (debug JSON)
    pass_a_filename = f"{base_name}_events.json"
    with open(pass_a_filename, 'w') as f:
        json.dump(midi_events_data, f, indent=2)
    print(f"  Saved debug events to: {pass_a_filename}")
    print(f"  Events: {len(midi_events_data['events'])}")
    print(f"  Ticks per beat: {midi_events_data['ticks_per_beat']}")
    print(f"  Tempo: {midi_events_data['tempo_bpm']} BPM")
    
    # Pass B: Convert to YM2151 log JSON
    print("\nPass B: Converting to YM2151 log...")
    ym2151_log = convert_to_ym2151_log(midi_events_data)
    
    # Save Pass B output (final JSON)
    pass_b_filename = f"{base_name}_ym2151.json"
    with open(pass_b_filename, 'w') as f:
        json.dump(ym2151_log, f, indent=2)
    print(f"  Saved YM2151 log to: {pass_b_filename}")
    print(f"  YM2151 events: {ym2151_log['event_count']}")
    
    print("\nConversion complete!")


if __name__ == '__main__':
    main()

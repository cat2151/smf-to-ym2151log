# smf-to-ym2151log

Convert Standard MIDI Files (SMF) to YM2151 register write log in JSON format.

## Features

- **2-Pass Processing**:
  - **Pass A**: Converts MIDI file to intermediate events JSON (for debugging)
  - **Pass B**: Converts events to YM2151 register write log JSON (final output)
- **Test-Driven Development**: Comprehensive unit tests
- **Modular Design**: Each source file kept to ~100 lines
- **Compatible Format**: Outputs JSON format compatible with [ym2151-zig-cc](https://github.com/cat2151/ym2151-zig-cc)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python smf_to_ym2151log.py <midi_file>
```

### Example

```bash
# Create a test MIDI file
python create_test_midi.py

# Convert it to YM2151 log
python smf_to_ym2151log.py test.mid
```

This will generate:
- `test_events.json` - Pass A output (debug events)
- `test_ym2151.json` - Pass B output (YM2151 log)

## Output Format

The YM2151 log JSON follows this format:

```json
{
  "event_count": 50,
  "events": [
    {"time": 0, "addr": "0x08", "data": "0x00", "is_data": 0},
    ...
  ]
}
```

Where:
- `time`: Sample time (integer, at 55930 Hz sample rate)
- `addr`: YM2151 register address (hex string)
- `data`: Data to write (hex string)
- `is_data`: 0 for address write, 1 for data write

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Project Structure

```
smf-to-ym2151log/
├── src/
│   ├── __init__.py
│   ├── midi_parser.py       # Pass A: MIDI to events
│   ├── midi_utils.py        # MIDI utility functions
│   └── ym2151_converter.py  # Pass B: Events to YM2151 log
├── tests/
│   ├── __init__.py
│   ├── test_midi_utils.py
│   └── test_ym2151_converter.py
├── smf_to_ym2151log.py      # Main script
├── create_test_midi.py      # Test MIDI file generator
└── requirements.txt
```

## Libraries Used

- **mido**: MIDI file parsing and manipulation

## License

See [LICENSE](LICENSE) file.
"""
YM2151 initialization module.
Handles channel initialization and default parameter setup.
"""


def initialize_channel_events(channel, sample_time=0):
    """
    Generate initialization events for a YM2151 channel.
    
    Args:
        channel: Channel number (0-7)
        sample_time: Time in samples when to initialize
        
    Returns:
        list: List of register write events
    """
    events = []
    
    # RL_FB_CONNECT
    events.append({
        'time': sample_time,
        'addr': f'0x{0x20 + channel:02X}',
        'data': '0xC7',
        'is_data': 0
    })
    
    # PMS/AMS
    events.append({
        'time': sample_time,
        'addr': f'0x{0x38 + channel:02X}',
        'data': '0x00',
        'is_data': 0
    })
    
    # Configure operators
    for op in range(4):
        slot = channel + (op * 8)
        
        # DT1/MUL
        events.append({
            'time': sample_time,
            'addr': f'0x{0x40 + slot:02X}',
            'data': '0x01',
            'is_data': 0
        })
        
        # TL (Total Level)
        if op == 0:
            tl_value = 0x00  # Max volume for carrier
        else:
            tl_value = 0x7F  # Silent for modulators
            
        events.append({
            'time': sample_time,
            'addr': f'0x{0x60 + slot:02X}',
            'data': f'0x{tl_value:02X}',
            'is_data': 0
        })
        
        # KS/AR
        events.append({
            'time': sample_time,
            'addr': f'0x{0x80 + slot:02X}',
            'data': '0x1F',
            'is_data': 0
        })
        
        # AMS/D1R
        events.append({
            'time': sample_time,
            'addr': f'0x{0xA0 + slot:02X}',
            'data': '0x05',
            'is_data': 0
        })
        
        # DT2/D2R
        events.append({
            'time': sample_time,
            'addr': f'0x{0xC0 + slot:02X}',
            'data': '0x05',
            'is_data': 0
        })
        
        # D1L/RR
        events.append({
            'time': sample_time,
            'addr': f'0x{0xE0 + slot:02X}',
            'data': '0xF7',
            'is_data': 0
        })
    
    return events

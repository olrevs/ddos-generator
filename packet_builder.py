import random
import string

def generate_delay_for_packet():
    """Generate random interval between sending packet in sec"""
    return round(random.uniform(0,0.5), 2)

def generate_payload(symbols_count=100):
    """Generate random payload for packet.
    
    Arugment:
    symbols_count -- generate sequence of random digits and symbols (default 100)

    """
    letters_and_digits = string.ascii_letters + string.digits

    return ''.join(random.choice(letters_and_digits) for i in range(random.randint(1, symbols_count)))

def generate_ttl():
    """Generate random TTL for packet between 0 and 255"""
    return random.randint(0,255)
import random
import string

def generate_delay_for_packet():
    """Generate random interval between sending packet in sec"""
    return round(random.uniform(0, 0.5), 2)

def generate_payload(min_count=1, max_count=1400):
    """Generate payload for packet with random symbols and digits beetween min and max symbols count.
    
    Arugment:
    min_count -- the minimum count of symbols in sequence (default 1)
    max_count -- the maximum count of symbols in sequence (default 1400)

    """
    letters_and_digits = string.ascii_letters + string.digits

    return ''.join(random.choice(letters_and_digits) for i in range(random.randint(min_count, max_count)))

def generate_ttl():
    """Generate random TTL for packet between 0 and 255"""
    return random.randint(0, 255)

def generate_fragsize():
    """Generate random fragment size for packet between 1 and 1400"""
    return random.randint(1, 1400)
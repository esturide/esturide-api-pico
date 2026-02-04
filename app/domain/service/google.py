decode_gps_from_google = lambda direction: (direction.get('lat'), direction.get('lng'))


class GoogleService:
    def __init__(self, gmaps):
        self.gmaps = gmaps
        self.components = {
            "country": "MX"
        }

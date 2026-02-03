decode_gps_from_google = lambda direction: (direction.get_from_user('lat'), direction.get_from_user('lng'))


class GoogleService:
    def __init__(self, gmaps):
        self.gmaps = gmaps
        self.components = {
            "country": "MX"
        }

from aredis_om import EmbeddedJsonModel


class GeoLocationEmbedded(EmbeddedJsonModel):
    latitude: float
    longitude: float

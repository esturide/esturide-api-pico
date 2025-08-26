import functools
from shapely.geometry import Point, Polygon, MultiPolygon

from app.shared.scheme.location import GeoLocationModel


class LocationService:
    GDL = Polygon([(-103.38, 20.67), (-103.35, 20.67), (-103.35, 20.65), (-103.38, 20.65)])
    ZAPOPAN = Polygon([(-103.45, 20.75), (-103.40, 20.75), (-103.40, 20.70), (-103.45, 20.70)])
    TLAQUEPAQUE = Polygon([(-103.35, 20.65), (-103.30, 20.65), (-103.30, 20.60), (-103.35, 20.60)])

    def __init__(self):
        self.__perimeter_zmg = MultiPolygon([self.GDL, self.ZAPOPAN, self.TLAQUEPAQUE]).buffer(0.1)

    @property
    def perimeter_zmg(self):
        return self.__perimeter_zmg

    def is_local(self, location: tuple[float, float] | GeoLocationModel) -> bool:
        if isinstance(location, tuple):
            return self.perimeter_zmg.contains(
                Point(location[0], location[1])
            )
        elif isinstance(location, GeoLocationModel):
            return self.perimeter_zmg.contains(
                Point(location.longitude, location.latitude)
            )

        return False

@functools.lru_cache
def get_location_service():
    return LocationService()

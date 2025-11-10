import dataclasses
import datetime
from typing import Set, Optional, Tuple, List

import polyline

from app.domain.service.google import GoogleService, decode_gps_from_google
from app.shared.pattern.singleton import Singleton
from app.shared.utils import async_task


@dataclasses.dataclass
class RouteResult:
    route: List[Tuple[float, float]]
    stoppingpoints: List[Tuple[float, float]]
    steps: List[Tuple[float, float]]


class RouteService(GoogleService, metaclass=Singleton):
    async def routing(self, origin: str, destination: str, waypoints: Set[str], time_start: Optional[datetime.datetime] = None) -> List[RouteResult]:
        def set_routing(origin, destination, waypoints, time_start):
            directions = self.gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                mode="driving",
                departure_time=time_start,
            )

            steps = []
            all_routes_data = []

            for direction in directions:
                for leg in direction['legs']:
                    for step in leg['steps']:
                        points = polyline.decode(step['polyline']['points'])
                        steps.extend(points)

                stoppingpoints = []

                if len(waypoints) > 0:
                    starting = decode_gps_from_google(direction["legs"][0]["start_location"])

                    stoppingpoints.append(starting)

                    for location in direction["legs"]:
                        stoppingpoints.append(decode_gps_from_google(location["end_location"]))
                else:
                    starting = decode_gps_from_google(direction["legs"][0]["start_location"])
                    finished = decode_gps_from_google(direction["legs"][0]["end_location"])

                    stoppingpoints = [
                        starting,
                        finished
                    ]

                route = polyline.decode(direction['overview_polyline']['points'])

                all_routes_data.append(
                    RouteResult(
                        route=route,
                        stoppingpoints=stoppingpoints,
                        steps=steps
                    )
                )

            return all_routes_data


        if time_start is None:
            time_start = datetime.datetime.now()

        return await async_task(set_routing, origin, destination, list(waypoints), time_start)

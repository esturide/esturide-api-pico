import datetime

import numpy as np

import polyline

from app.domain.service.google import GoogleService, decode_gps_from_google
from app.shared.pattern.singleton import Singleton
from app.shared.utils import async_task


class RouteService(GoogleService, metaclass=Singleton):
    async def routing(self, origin, destination, waypoints, time_start=None):
        def set_routing(origin, destination, waypoints, time_start):
            if time_start is None:
                time_start = datetime.datetime.now()

            directions = self.gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                mode="driving",
                departure_time=time_start,
                components=self.components
            )

            steps = []

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

                yield np.array(route), np.array(stoppingpoints), np.array(steps)


        return async_task(set_routing, origin, destination, waypoints, time_start)

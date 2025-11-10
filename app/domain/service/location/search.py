from app.domain.service.google import GoogleService, decode_gps_from_google
from app.shared.pattern.singleton import Singleton
from app.shared.utils import async_task


class SearchService(GoogleService, metaclass=Singleton):
    async def search(self, address: str):
        def search_address(address):
            all_results = []

            if results := self.gmaps.geocode(address, components=self.components):
                for result in results:
                    formatted_address = result['formatted_address']
                    location = result['geometry']['location']

                    all_results.append(
                        (formatted_address, decode_gps_from_google(location))
                    )
            else:
                raise ValueError(f"Address {address} not found.")

            return all_results


        return await async_task(search_address, address)

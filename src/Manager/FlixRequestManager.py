import requests
from src.Packages.ResultPackage import ResultPackage
from src.Packages.InformationPackage import InformationPackage as IPack


class FlixRequestManager:
    provider = "Flix"
    apiKey = "k8LKgcuFoHnN5x/NdDYD6QSvjB4="
    url = "https://api.flixbus.com/mobile/v1/trip/search.json"

    headers = {
        "Content-Type": "application/json",
        "X-API-Authentication": "k8LKgcuFoHnN5x/NdDYD6QSvjB4=",
        "User-Agent": "FlixBus/3.3 (iPhone; iOS 9.3.4; Scale/2.00)",
        "X-User-Country": "de",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    trip = {
        "search_by": "cities",  # 'stations'
        "currency": "EUR",
        "adult": 1,
        "children": 0,
        "bikes": 0,
    }

    def setData(self, ipack, stationFrom, stationTo, date):
        """get the relevant Data out off the IPack"""
        if isinstance(ipack, IPack):
            self.trip["departure_date"] = ".".join(
                [
                    ("0" + str(date[0]))[-2:],
                    ("0" + str(date[1]))[-2:],
                    str(date[2]),
                ]
            )  # Convert Date list to Datestring (z.B. 31.02.2020)
            self.trip["from"] = stationFrom['flixId']
            self.trip["to"] = stationTo['flixId']
            self.trip['adult'] = ipack.traveller if ipack.traveller > 0 else 1

    def makeRequest(self):
        """make the final Request call after set_from_ipack"""
        result_packs = []
        response = requests.get(
            self.url, params=self.trip, headers=self.headers)
        for trip in response.json()["trips"]:
            for item in trip["items"]:
                if item["status"] == "full":
                    continue
                result_packs.append(
                    ResultPackage(trip["from"]["name"],
                                  trip["to"]["name"],
                                  self.provider,
                                  item)
                )
        return result_packs

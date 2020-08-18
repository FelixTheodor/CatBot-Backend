import json


def getStationNames(body):
    name = body['name']
    with open("src/Data/stations.json") as stations:
        stationJson = json.load(stations)

        def filterName(x):
            return name.lower() in x['name'].lower()

        res = list(filter(filterName, stationJson))
    return [o['name'] for o in res]

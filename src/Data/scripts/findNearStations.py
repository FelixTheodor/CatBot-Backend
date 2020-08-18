from math import sin, cos, sqrt, atan2, radians
import json
import copy
from operator import itemgetter

# this script is needed to create the database
# unless the database needs an update, you dont need to look at it


def getDistance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


f = open("src/Data/stations.json", "r")
w = open("src/Data/stations3.json", "w")
w.write("[\n")

data = json.load(f)
new_json = copy.deepcopy(data)
for station in data:
    allDistances = []
    lat1 = station["coordinates"]["latitude"]
    lon1 = station["coordinates"]["longitude"]
    for otherStation in data:
        if station["name"] == otherStation["name"]:
            continue
        lat2 = otherStation["coordinates"]["latitude"]
        lon2 = otherStation["coordinates"]["longitude"]
        dist = getDistance(lat1, lon1, lat2, lon2)
        allDistances.append([otherStation["name"], dist])

    station["nearestStations"] = sorted(allDistances, key=itemgetter(1))[0:20]
    json.dump(station, w, indent=4, ensure_ascii=False)
    w.write(",\n")
w.write("\n]")

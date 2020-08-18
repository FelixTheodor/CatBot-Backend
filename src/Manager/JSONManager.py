from src.Packages.AnswerPackage import AnswerPackage as APack
from src.Packages.InformationPackage import InformationPackage as IPack
import json
import time
from math import sin, cos, sqrt, atan2, radians
from src.Worker.Helper import load, computeDistance

# this class handles all interactions with jsons:
# (un)packing all sorts of packages
# holding and handling the json-database of all stations


class JSONManager:
    @load
    def __init__(self):
        f = open("src/Data/stations.json")
        self.data = json.load(f)
        f.close()
        time.sleep(1)

    def createJSONFromPackages(self, apackage, ipackage):
        dic = {"answerPackage": json.loads(
            apackage), "informationPackage": json.loads(ipackage)}

        return(json.dumps(dic))

    def convertJSONToIPack(self, jsondic):
        ip = IPack()
        ip.setFromJSON(jsondic["informationPackage"])
        return ip

    def getMessage(self, jsondic):
        return (jsondic["message"])

    def getAllCityNames(self):
        cityNames = []
        for li in self.data:
            cityNames.append(li["name"])

        return cityNames

    def getNearestStations(self, ip):
        cityNames = []
        distance = 0
        for li in self.data:
            if li["name"] == ip.origin[0]:
                for li2 in self.data:
                    if li2["name"] == ip.destination[0]:
                        lat1 = li["coordinates"]["latitude"]
                        lon1 = li["coordinates"]["longitude"]
                        lat2 = li2["coordinates"]["latitude"]
                        lon2 = li2["coordinates"]["longitude"]
                        distance = computeDistance(lat1, lon1, lat2, lon2)
                        break
                for city in li["nearestStations"]:
                    if city[1] <= (distance / 10):
                        cityNames.append(city[0])
        return cityNames

    def getDistance(self, origin, destination):
        o_lat = 0
        o_lon = 0
        d_lat = 0
        d_lon = 0
        for li in self.data:
            if li["name"] == origin:
                o_lat = li["coordinates"]["latitude"]
                o_lon = li["coordinates"]["longitude"]
            elif li["name"] == destination:
                d_lat = li["coordinates"]["latitude"]
                d_lon = li["coordinates"]["longitude"]
            else:
                continue
        if o_lat != 0 and o_lon != 0 and d_lat != 0 and d_lon != 0:
            return computeDistance(o_lat, o_lon, d_lat, d_lon)
        else:
            return 0

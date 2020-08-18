import json
from datetime import datetime
from src.Packages.InformationPackage import InformationPackage as IPack
from src.Manager.DbRequestManager import DbRequestManager
from src.Manager.FlixRequestManager import FlixRequestManager


class RequestManager:
    """Makes a Request for DB and Flix"""

    db_request = DbRequestManager()
    flix_requst = FlixRequestManager()
    stationsFrom = []
    stattionsTo = []
    ipack = None

    def setFromDict(self, infos):
        if isinstance(infos, dict):
            ipack = IPack()
            ipack.setFromJSON(infos)
            self.setFromIpack(ipack)

    def setFromIpack(self, ipack):
        """Gives data to DB and Flix"""
        self.stationsFrom = self.getStationNumbers(ipack.origin)
        self.stationsTo = self.getStationNumbers(ipack.destination)
        if isinstance(ipack, IPack):
            self.ipack = ipack

    def makeRequest(self):
        """makes the Request"""
        multicity_res = []
        for date in self.ipack.date:
            for stationFrom in self.stationsFrom:
                for stationTo in self.stationsTo:
                    self.db_request.setData(
                        self.ipack, stationFrom, stationTo, date)
                    self.flix_requst.setData(
                        self.ipack, stationFrom, stationTo, date)
                    response_db = self.myFilter(self.db_request.makeRequest())
                    response_flix = self.myFilter(
                        self.flix_requst.makeRequest())
                    results_jsons = [p.toJSON()
                                     for p in [*response_db, *response_flix]]
                    multicity_res = [*multicity_res, *results_jsons]
        res = f"[{' ,'.join(multicity_res)}]"
        return res

    def myFilter(self, res):
        return [o for o in res if
                self.checkTime(o.departure['timestamp'], self.ipack.time)
                and self.checkPrice(o.price, self.ipack.budget)
                and self.checkTransvers(o.transfers, self.ipack.transfers)]

    @ staticmethod
    def checkTransvers(transvers, revTransvers):
        if revTransvers == -1:
            return True
        return transvers <= revTransvers

    @ staticmethod
    def checkPrice(price, budget):
        if budget == -1:
            return True
        return price <= budget

    @ staticmethod
    def checkTime(time, revTime):
        if len(revTime) == 0:
            return True
        timeObj = datetime.fromtimestamp(time)
        timeCounter = int(str(timeObj.strftime("%H")) +
                          str(timeObj.strftime("%M")))
        revTimeCounter = int(str(revTime[0])+('0'+str(revTime[1]))[-2:])

        return timeCounter > revTimeCounter

    @ staticmethod
    def getStationNumbers(names):
        """get dbID and flixId from Station out off json"""
        result = []
        with open("src/Data/stations.json") as stations:
            stationJson = json.load(stations)

            def filterName(x):
                return name in x['name']

            for name in names:
                res = list(filter(filterName, stationJson))
                if len(res) == 1:
                    result.append(res[0])
            return result
        return False

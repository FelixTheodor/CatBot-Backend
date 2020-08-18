"""Scripts startSparpreisSuche"""
import requests
from src.Packages.ResultPackage import ResultPackage


class DbRequestManager:
    """class makes a Request for DBSparpreis"""

    provider = "DB"
    URL = "https://ps.bahn.de/preissuche/preissuche/psc_service.go"
    PARAMS = {
        "service": "pscangebotsuche",
        "lang": "en",
        "country": "GBR",
        "data": r'{"bic":false,"c":"2","d":"008000263","device":"HANDY"'
        + r',"dir":1,"dt":"23.03.20","dur":1440,"ohneICE":false,'
        + r'"os":"Android REL 26"'
        + r',"pscexpires":"","s":"008096022","sv":true,"t":"0:00","tct":0,'
        + r'"travellers":[{"alter":"","bc":"0","bcDesc":"0","typ":"E"}],'
        + r'"v":"19100000"}',
    }
    HEADERS = {
        "charset": "utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0;"
        + " Custom Phone_8 Build/OPR6.170623.017)",
        "Host": "ps.bahn.de",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Length": "0",
    }
    trip = {}

    def makeRequest(self):
        """start the complete Request from names to answerArray"""
        data = self.makeServerRequest(
            self.trip["ori"],
            self.trip["des"],
            self.trip["date"],
            self.trip['traveller'],
            self.trip['time']
        )
        return self.processAnswer(data)

    def makeServerRequest(self, start, dest, date, traveller, time):
        """make the Request"""
        self.PARAMS["data"] = (
            r'{"bic":false,"c":"2","d":"'
            + dest
            + r'","device":"HANDY","dir":1,"dt":"'
            + date
            + r'","dur":1440,"ohneICE":false,'
            + r'"os":"Android REL 26","pscexpires":"","s":"'
            + start
            + r'","sv":true,"t":"'
            + time
            + r'","tct":0,"travellers":'
            + r'['
            + (r'{"alter":"","bc":"0","bcDesc":"0","typ":"E"},'*traveller)[:-1]
            + r']'
            + r',"v":"19100000"}'
        )
        response = requests.post(
            self.URL, params=self.PARAMS, headers=self.HEADERS)
        return response.json()

    @staticmethod
    def getImportant(a, v):
        """get Important Information out of respose"""
        important = {
            "price": a["p"],
            "date": v["dt"],
            "duration": v["dur"],
            "umstiege": v["nt"],
            "trainsTyp": v["eg"],
            "connection": [
                {
                    "start": i["sn"],
                    "ziel": i["dn"],
                    "Zugnummer": i["tn"],
                    "departure": i["dep"]["m"],
                    "arrival": i["arr"]["m"],
                }
                for i in v["trains"]
            ],
        }
        return important

    def processAnswer(self, data):
        """Get the Important Details from the Answer"""
        AngebotArray = []
        if 'angebote' in data.keys():
            AngebotArray = [
                data["angebote"][i]
                for i in data["angebote"].keys()
            ]
        res = []
        for a in AngebotArray:
            for b in [self.getImportant(a, data["verbindungen"][v]) for v in a["sids"]]:
                jsn = {
                    "status": "Ready",
                    "departure": {
                        "timestamp":
                            int(b["connection"][0]["departure"]) / 1000,
                        "tz": "GMT+02:00",
                    },
                    "arrival": {
                        "timestamp":
                            int(b["connection"][-1]["arrival"]) / 1000,
                        "tz": "GMT+02:00",
                    },
                    "duration": {
                        "hour": int(b["duration"].split(":")[0]),
                        "minutes": int(b["duration"].split(":")[1]),
                    },
                    "price_total_sum": b["price"],
                    "interconnection_transfers": len(b["connection"]) - 1,
                }
                res.append(
                    ResultPackage(
                        b["connection"][0]["start"],
                        b["connection"][-1]["ziel"],
                        self.provider,
                        jsn
                    )
                )
        return res

    def setData(self, ipack, stationFrom, stationTo, date):
        """get Trip information from ipack"""
        self.trip["ori"] = "00" + stationFrom['dbId']
        self.trip["des"] = "00" + stationTo['dbId']
        self.trip['traveller'] = ipack.traveller if ipack.traveller > 0 else 1
        self.trip["date"] = ".".join(
            [
                ("0" + str(date[0]))[-2:],
                ("0" + str(date[1]))[-2:],
                str(date[2])[-2:],
            ]
        )  # Convert Date list to Datestring (z.B. 31.02.20)
        if len(ipack.time) == 2:
            self.trip['time'] = str(ipack.time[0]) + \
                ":"+("0"+str(ipack.time[1]))[-2:]
        else:
            self.trip['time'] = '0:00'

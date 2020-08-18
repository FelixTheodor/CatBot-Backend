from src.Packages.Package import Package

# this package holds the results of a query


class ResultPackage(Package):
    status = None  # String
    origin = None  # String
    destination = None  # String
    departure = None  # dict {'timestap':,'tz':}
    arrival = None  # dict {'timestap':,'tz':}
    duration = None  # dict {'hour':,'minutes':}
    price = None  # float
    transfers = None  # int
    provider = None  # String
    link = None  # String

    def __init__(self, origin, destination, provider, jsn):
        super().__init__()
        self.setOrigin(origin)
        self.setDestination(destination)
        self.setProvider(provider)
        self.setFromJSON(jsn)

    # calls all sets from dict
    def setFromJSON(self, jsn):
        self.setStatus(jsn["status"])
        # self.setOrigin(jsn["origin"])
        # self.setDestination(jsn["destination"])
        self.setDeparture(jsn["departure"])
        self.setArrival(jsn["arrival"])
        self.setDuration(jsn["duration"])
        self.setPrice(jsn["price_total_sum"])
        self.setTransfers(jsn["interconnection_transfers"])

    # Status
    def setStatus(self, status):
        if type(status) is str:
            self.status = status
        else:
            self.status = False

    # origin
    def setOrigin(self, origin):
        if type(origin) is str:
            self.origin = origin

        elif type(origin) is list:
            self.origin = origin[0]

        else:
            pass  # Mistake

    # destination
    def setDestination(self, destination):
        if type(destination) is list:
            self.destination = destination[0]

        elif type(destination) is str:
            self.destination = destination

        else:
            pass  # Mistake

        # Provider
    def setProvider(self, provider):
        if type(provider) is str:
            self.provider = provider
        else:
            pass  # Mistake

    def setLink(self, link):
        if type(link) is str:
            self.link = link
        else:
            pass  # Mistake

    # Departure
    def setDeparture(self, date):
        if type(date) is dict:
            self.departure = date

    # Arrival
    def setArrival(self, date):
        if type(date) is dict:
            self.arrival = date

    # Durration
    def setDuration(self, dur):
        if type(dur) is dict:
            self.duration = dur

    # price
    def setPrice(self, price):
        if(type(price) is str):
            self.price = float(price.replace(',', '.'))
        elif type(price) is int or float:
            self.price = price

    # transfers

    def setTransfers(self, transfers):
        if type(transfers) is int:
            self.transfers = transfers
        elif type(transfers) is str:
            self.transfers = int(transfers)
        elif type(transfers) is list:
            self.transfers = len(transfers)

from src.Packages.Package import Package

# this is the InformationPackage, conatining all informationen needed for the query
# the NLU on the Server never saves this,
# so the front- and backend always send the full package to each other


class InformationPackage(Package):
    origin = None  # list
    destination = None  # list
    date = None  # list of lists
    time = []  # list
    traveller = -1  # int
    budget = -1  # int
    transfers = -1  # int
    state = ""  # string
    repeat = False  # bool

    def __init__(self):
        super().__init__()

    def fullReset(self):
        self.origin = []  # list
        self.destination = []  # list
        self.date = []  # list of lists
        self.time = []  # list
        self.traveller = -1  # int
        self.budget = -1  # int
        self.transfers = -1  # int
        self.state = ""  # string
        self.repeat = False  # bool

    # calls all sets from dict
    def setFromJSON(self, jsn):
        self.setBudget(jsn["budget"])
        self.setDate(jsn["date"])
        self.setDestination(jsn["destination"])
        self.setOrigin(jsn["origin"])
        self.setState(jsn["state"])
        self.setTime(jsn["time"])
        self.setTransfers(jsn["transfers"])
        self.setTraveller(jsn["traveller"])

    # returns true if all optional parameters have values
    def hasNoBlanks(self):
        return (
            self.time and self.traveller != -1
            and self.budget != -1 and self.transfers != -1
        )

    # origin
    def setOrigin(self, origin):
        if isinstance(origin, list):
            self.origin = origin

        elif isinstance(origin, str):
            self.origin = [origin]

        else:
            pass  # Mistake

    def appendOrigin(self, origin):
        if self.origin is not None:
            if len(self.origin) == 0:
                if isinstance(origin, str):
                    self.origin = [origin]
                elif isinstance(origin, list):
                    self.origin = origin
                else:
                    pass  # Mistake
            else:
                if isinstance(origin, str):
                    self.origin.append(origin)
                elif isinstance(origin, list):
                    for x in origin:
                        self.origin.append(x)
                else:
                    pass  # Mistake

        else:
            if isinstance(origin, str):
                self.origin = [origin]
            elif isinstance(origin, str):
                self.origin = origin
            else:
                pass  # Mistake

    # destination
    def setDestination(self, destination):
        if isinstance(destination, list):
            self.destination = destination

        elif isinstance(destination, str):
            self.destination = [destination]

        else:
            pass  # Mistake

    def appendDestination(self, destination):
        if self.destination is not None:
            if len(self.destination) == 0:
                if isinstance(destination, str):
                    self.destination = [destination]
                elif isinstance(destination, list):
                    self.destination = destination
                else:
                    pass  # Mistake
            else:
                if isinstance(destination, str):
                    self.destination.append(destination)
                elif isinstance(destination, list):
                    for x in destination:
                        self.destination.append(x)
                else:
                    pass  # Mistake

        else:
            if isinstance(destination, str):
                self.destination = [destination]
            elif isinstance(destination, list):
                self.destination = destination
            else:
                pass  # Mistake

    # date
    def setDate(self, date):
        if isinstance(date, list):
            self.date = date

    def expandDate(self, prev_day, next_day):
        self.date.insert(0, list(map(int, prev_day)))
        self.date.append(list(map(int, next_day)))

    # time
    def setTime(self, time):
        if isinstance(time, list):
            self.time = time

    # budget
    def setBudget(self, budget):
        if isinstance(budget, int) or isinstance(budget, float):
            self.budget = budget

    # transfers
    def setTransfers(self, transfers):
        if isinstance(transfers, int):
            self.transfers = transfers

    # traveller
    def setTraveller(self, traveller):
        if isinstance(traveller, int):
            self.traveller = traveller

    # state
    def setState(self, state):
        if isinstance(state, str):
            self.state = state

    def setRepeat(self, rep):
        self.repeat = rep

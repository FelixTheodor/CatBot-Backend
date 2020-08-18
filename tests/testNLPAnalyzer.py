from src.Worker.Analyzer import Analyzer
from src.Manager.JSONManager import JSONManager
from src.Packages.InformationPackage import InformationPackage
from src.Data.Lexicon import Lexicon
import unittest
import time

# some, but not all states are testable
# it can be used to debug the code and find errors
# furthermore, it can be used to understand the code
# feel free to expand or add new tests


class MyAnalyzeTests(unittest.TestCase):
    Ana = Analyzer(JSONManager(), isTest=True)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def testBasicType(self):
        IPack = InformationPackage()
        msg = "Test."
        self.assertEqual(type(self.Ana.analyze(msg, IPack)),
                         InformationPackage)

    def testGreeting(self):
        IPack = InformationPackage()
        msg = Lexicon.Internals.StartChat
        state = Lexicon.Internals.Y_N_Tutorial
        self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

    def testYesAndNo(self):
        IPack = InformationPackage()
        # Yes
        state = Lexicon.Internals.StartTutorial
        msgs = ["ja", "japp", "gern", "klar"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Y_N_Tutorial
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)
        # No
        state = Lexicon.Internals.Origin
        msgs = ["nein", "nee", "nö", "nope"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Y_N_Tutorial
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

    def testRepeat(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.StartTutorial
        msg = "hrungendunz"
        self.assertTrue(self.Ana.analyze(msg, IPack).repeat)

    def testFindCitys(self):
        IPack = InformationPackage()
        city = ["Bochum"]
        msgs = ["Ich wohne in Bochum", "bochum", "Bochum oder so",
                "Bochum wäre klasse, also finde ich jedenfalls. Was meinst du denn Hasi"]  # long inputs
        for msg in msgs:
            IPack.state = Lexicon.Internals.Origin
            self.assertTrue(self.Ana.analyze(msg, IPack).origin == city)

        state = Lexicon.Internals.Y_N_Origin
        msgs = ["Also ich fände ja Brochum als Startpunkt gut",
                "Mühnchen", "Ich denke, Bochumr"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Origin
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

        state = Lexicon.Internals.OriginCorrection
        msgs = ["Mühnchänl wär supi", "was willst du denn von mir??"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Origin
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

    def testDate(self):
        IPack = InformationPackage()
        state = Lexicon.Internals.FlexibleDate
        msgs = ["03.10.2020", "03 10", "03/10", "03.10",
                "3 Oktober", "3. Oktober", "3.Oktober"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Date
            self.assertTrue(self.Ana.analyze(
                msg, IPack).date == [[3, 10, 2020]], msg=f"Message: {msg}")
        msgs = ["morgen", "übermorgen", "10.02"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Date
            self.assertTrue(self.Ana.analyze(
                msg, IPack).state == state, msg=f"Message: {msg}")
        msgs = ["31.10.2007", "12.11.2015", "10.02.2020"]
        state = Lexicon.Internals.PastDate
        for msg in msgs:
            IPack.state = Lexicon.Internals.Date
            self.assertTrue(self.Ana.analyze(
                msg, IPack).state == state, msg=f"Message: {msg}")

        msgs = ["test", "was willst du?"]
        for msg in msgs:
            IPack.state = Lexicon.Internals.Date
            self.assertTrue(self.Ana.analyze(
                msg, IPack).repeat, msg=f"Message: {msg}")

    def testExpandDate(self):
        IPack = InformationPackage()
        IPack.setDate([[31, 8, 2023]])
        IPack.state = Lexicon.Internals.FlexibleDate
        self.assertTrue(self.Ana.analyze(
            "ja", IPack).date == [[30, 8, 2023], [31, 8, 2023], [1, 9, 2023]], msg="expanding_date not working")

    def testOpen(self):
        IPack = InformationPackage()
        IPack.traveller = -1
        IPack.budget = -1
        IPack.time = []
        IPack.transfers = -1

        msgs = ["Ich würde gerne wenig Geld ausgeben",
                "hab ein begrentes Budget", "bin knapp bei Kasse"]
        state = Lexicon.Internals.Budget
        for msg in msgs:
            IPack.state = Lexicon.Internals.Open
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

        msgs = ["ich würde gerne mehrere plätze buchen",
                "wir sind viele", "würde gerne mit mehr leuten fahren"]
        state = Lexicon.Internals.Traveller
        for msg in msgs:
            IPack.state = Lexicon.Internals.Open
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

        msgs = ["ich würde gerne früh los",
                "will zu einer bestimmten uhrzeit los", "abfahrtstermin einstellen"]
        state = Lexicon.Internals.Time
        for msg in msgs:
            IPack.state = Lexicon.Internals.Open
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

        msgs = ["ich würde gerne nicht so oft umsteigen",
                "meine toleranz ist gering wegen halten", "viele stopps und ich raste aus!"]
        state = Lexicon.Internals.Transfers
        for msg in msgs:
            IPack.state = Lexicon.Internals.Open
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

        msgs = ["kannst anfangen zu suchen",
                "starte bitte", "zeig verbindungen"]
        state = Lexicon.Internals.Query
        for msg in msgs:
            IPack.state = Lexicon.Internals.Open
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)

    def testTime(self):
        IPack = InformationPackage()
        msgs = ["7.30", "7:30",
                "irgendwann mittags", "abends wäre gut, eher spät"]
        state = Lexicon.Internals.Open
        for msg in msgs:
            IPack.state = Lexicon.Internals.Time
            self.assertTrue(self.Ana.analyze(msg, IPack).state == state)
        IPack.state = Lexicon.Internals.Time
        self.assertTrue(self.Ana.analyze("halb 9", IPack).time == [8, 30])
        IPack.state = Lexicon.Internals.Time
        self.assertTrue(self.Ana.analyze(
            "viertel nach neun", IPack).time == [9, 15])
        IPack.state = Lexicon.Internals.Time
        self.assertTrue(self.Ana.analyze(
            "viertel vor 9", IPack).time == [8, 45])
        IPack.state = Lexicon.Internals.Time
        self.assertTrue(self.Ana.analyze(
            "19 Uhr dreißig", IPack).time == [19, 30])
        IPack.state = Lexicon.Internals.Time
        self.assertTrue(self.Ana.analyze(
            "halb 8 abends", IPack).time == [19, 30])

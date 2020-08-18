from src.Worker.AnswerFormulator import AnswerFormulator
from src.Manager.JSONManager import JSONManager
from src.Packages.InformationPackage import InformationPackage
from src.Data.Lexicon import Lexicon
import unittest
import time

# some, but not all states are testable
# it can be used to debug the code and find errors
# furthermore, it can be used to understand the code
# feel free to expand or add new tests


class MyAnswerTests(unittest.TestCase):
    AF = AnswerFormulator(JSONManager())

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def testGreeting(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.Y_N_Tutorial
        ap_msg = Lexicon.Output.ExplGreetings[0]
        self.assertTrue(ap_msg in self.AF.createAnswer(IPack).mainAnswer)

    def testTutorial(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.StartTutorial
        ap_msg = Lexicon.Output.TutorialMsg[0]
        self.assertTrue(ap_msg in self.AF.createAnswer(IPack).mainAnswer)

    def testMoreInformationsToChatbots(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.GiveMoreInformationsToChatbots
        ap_msg = Lexicon.Output.WikiToChatbots[0]
        self.assertTrue(ap_msg in self.AF.createAnswer(IPack).last)

    def testAskForOrigin(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.Origin
        ap_msgs = Lexicon.Output.AskForOrigin
        self.assertTrue(self.AF.createAnswer(IPack).mainAnswer in ap_msgs)

    def testFlexibleStartPoint(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.FlexibleStartPoint
        IPack.origin = ["Bochum"]
        IPack.destination = ["Bremen"]
        answer = self.AF.createAnswer(IPack).mainAnswer
        self.assertTrue("7 Städte" in answer)

    def testOpenStart(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.Open
        IPack.traveller = -1
        IPack.budget = -1
        IPack.time = []
        IPack.transfers = -1
        answer = self.AF.createAnswer(IPack).preface
        self.assertTrue(
            "alle Informationen" in answer)

    def testOpen3(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.Open
        IPack.traveller = -1
        IPack.budget = 200
        IPack.time = []
        IPack.transfers = -1
        answer = self.AF.createAnswer(IPack).mainAnswer
        self.assertTrue(
            "kannst du mir jetzt noch sagen" in answer)

    def testPetCustomer(self):
        IPack = InformationPackage()
        IPack.state = Lexicon.Internals.PetCustomer
        IPack.origin = ["Bochum"]
        IPack.destination = ["München"]
        answer = self.AF.createAnswer(IPack).mainAnswer
        self.assertTrue(
            "15.5 Kilogramm" in answer)

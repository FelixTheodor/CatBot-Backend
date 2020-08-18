from src.Packages.AnswerPackage import AnswerPackage
from src.Packages.InformationPackage import InformationPackage
from src.Manager.JSONManager import JSONManager
from src.Worker.Analyzer import Analyzer
from src.Worker.AnswerFormulator import AnswerFormulator
from src.Data.Lexicon import Lexicon, ChooseRandomAnswer
from src.Worker.ErrorChecker import ErrorChecker

# this class is the Entrypoint for the NLU
# holds all the components and manages its interactions


class DialogManager():
    def __init__(self):
        print("\nLoading Components of DialogManager:")
        self.jsm = JSONManager()
        self.err = ErrorChecker()
        self.af = AnswerFormulator(self.jsm)
        self.ana = Analyzer(self.jsm)
        print("\n\nDialogManager is initialized.")

    # Main-Method
    def processRequest(self, jsn):
        # extract the information-package from json
        ipack = self.jsm.convertJSONToIPack(jsn)
        # extract the message from json
        message = self.jsm.getMessage(jsn)
        # trigger the analysis via own analyzer
        returnIP = self.startAnalysis(message, ipack)
        # trigger the answer-formulator to get an answer
        returnAP = self.getAnswerFromAF(returnIP)
        # check for errors in the answer
        returnIP, returnAP = self.checkForErrors(returnIP, returnAP)
        # create an json that can be returned to the website
        returnJSON = self.jsm.createJSONFromPackages(
            returnAP.toJSON(), returnIP.toJSON())

        return returnJSON

    def getAnswerFromAF(self, ipack):
        ap = self.af.createAnswer(ipack)

        if ap is not None:
            if ap.filled:
                print("answerformulator done: found an answer.")
            else:
                print("WARN: Package unfilled")
        else:
            print("WARN: No Answer found.")
        return ap

    def startAnalysis(self, message, ipack):
        r_ipack = self.ana.analyze(message, ipack)

        print(f"analyzer done, state: {r_ipack.state}")

        return r_ipack

    def checkForErrors(self, returnIP, returnAP):
        return self.err.repareErrors(returnIP, returnAP)

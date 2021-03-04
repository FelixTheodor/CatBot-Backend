from src.Data.Lexicon import Lexicon, ChooseRandomAnswer
from src.Packages.AnswerPackage import AnswerPackage
from src.Worker.Helper import load, computeCO2
import time


class AnswerFormulatorNoPers:
    @load
    def __init__(self, jsn):
        self.jsn = jsn

    def createAnswer(self, ipack):
        ap = AnswerPackage()

        if ipack.state == Lexicon.Internals.Y_N_Tutorial:
            ap = self.initializeChat(ap)

        if ipack.state == Lexicon.Internals.StartTutorial:
            ap = self.startTutorial(ap)

        if ipack.state == Lexicon.Internals.GiveMoreInformationsToChatbots:
            ap = self.moreInformationsToChatbots(ap)

        if ipack.state == Lexicon.Internals.Origin:
            ap = self.askForOrigin(ap)

        if ipack.state == Lexicon.Internals.Y_N_Origin:
            ap = self.confirmOrigin(ap, ipack)

        if ipack.state == Lexicon.Internals.OriginCorrection:
            ap = self.startAutoCorrectionForOrigin(ap)

        if ipack.state == Lexicon.Internals.Destination:
            ap = self.askForDestination(ap)

        if ipack.state == Lexicon.Internals.Y_N_Destination:
            ap = self.confirmDestination(ap, ipack)

        if ipack.state == Lexicon.Internals.DestinationCorrection:
            ap = self.startAutoCorrectionForDestination(ap)

        if ipack.state == Lexicon.Internals.FlexibleStartPoint:
            ap = self.askForFlexibleStartpoint(ap, ipack)

        if ipack.state == Lexicon.Internals.ShowPossibleStartPoints:
            ap = self.showStartPoints(ap, ipack)

        if ipack.state == Lexicon.Internals.Date:
            ap = self.askForDate(ap)

        if ipack.state == Lexicon.Internals.PastDate:
            ap = self.dateIsInPast(ap)

        if ipack.state == Lexicon.Internals.FlexibleDate:
            ap = self.askForFlexDate(ap)

        if ipack.state == Lexicon.Internals.Open:
            ap = self.openAnswer(ap, ipack)

        if ipack.state == Lexicon.Internals.Time:
            ap = self.askForTime(ap)

        if ipack.state == Lexicon.Internals.Budget:
            ap = self.askForBudget(ap)

        if ipack.state == Lexicon.Internals.Traveller:
            ap = self.askForTraveller(ap)

        if ipack.state == Lexicon.Internals.Transfers:
            ap = self.askForTransfers(ap)

        if ipack.state == Lexicon.Internals.Query:
            ap = self.explainQuery(ap)

        if ipack.state == Lexicon.Internals.PetCustomer:
            ap = self.petCustomer(ap, ipack)

        if ipack.state == Lexicon.Internals.AskForAnotherStart:
            ap = self.askForStart(ap)

        if ipack.state == Lexicon.Internals.SayGoodbye:
            ap = self.sayGoodbye(ap)

        if ipack.state == Lexicon.Internals.OriginAgain:
            ap = self.originAgain(ap)

        return ap

    def formulateGeneralAnswer(self, ap, emotion, pre, msg, last):
        # if the state is well-defined the answers can just be pulled from the Lexicon
        preface = ChooseRandomAnswer(pre)
        message = ChooseRandomAnswer(msg)
        lastString = ChooseRandomAnswer(last)
        # the ap is filled with the answer strings
        ap.setAll(emotion, preface, message, lastString)

    def replaceAllCustomStrings(self, ap, listOfRepl):
        if "###" in ap.mainAnswer:
            for i in range(len(listOfRepl)):
                ap.mainAnswer = ap.mainAnswer.replace(
                    "###" + str(i) + "###", str(ChooseRandomAnswer(listOfRepl[i])))
        return ap

    def initializeChat(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.FirstGreetings,
                                    Lexicon.OutputNP.ExplGreetings,
                                    Lexicon.OutputNP.QuestGreetings)
        return ap

    def startTutorial(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.TutorialMsg,
                                    Lexicon.OutputNP.AskForUnderstanding)
        return ap

    def moreInformationsToChatbots(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.ConfirmationNeut,
                                    Lexicon.OutputNP.GiveMoreInfosToChatbots,
                                    Lexicon.OutputNP.WikiToChatbots)
        return ap

    def askForOrigin(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationNeut,
                                    Lexicon.OutputNP.AskForOrigin,
                                    Lexicon.OutputNP.Empty)
        return ap

    def confirmOrigin(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.ConfirmationThinking,
                                    Lexicon.OutputNP.AskForConfirmation,
                                    Lexicon.OutputNP.Empty)
        ap = self.replaceAllCustomStrings(
            ap, [ip.origin])
        return ap

    def startAutoCorrectionForOrigin(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationThinking,
                                    Lexicon.OutputNP.ExplainAutocorrection,
                                    Lexicon.OutputNP.AskForCitys)
        return ap

    def askForDestination(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationNeut,
                                    Lexicon.OutputNP.AskForDestination,
                                    Lexicon.OutputNP.Empty)
        return ap

    def confirmDestination(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.ConfirmationThinking,
                                    Lexicon.OutputNP.AskForConfirmation,
                                    Lexicon.OutputNP.Empty)
        ap = self.replaceAllCustomStrings(
            ap, [ip.destination])
        return ap

    def startAutoCorrectionForDestination(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationThinking,
                                    Lexicon.OutputNP.ExplainAutocorrection,
                                    Lexicon.OutputNP.AskForCitys)
        return ap

    def askForFlexibleStartpoint(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.AskFlexibleStartpoint,
                                    Lexicon.OutputNP.FSCookie)
        ap = self.replaceAllCustomStrings(
            ap, [[len(self.jsn.getNearestStations(ip))]])
        return ap

    def showStartPoints(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.LookingForInfo,
                                    Lexicon.OutputNP.GiveAllStartpoints,
                                    Lexicon.OutputNP.AskForStartponts)
        ap = self.replaceAllCustomStrings(
            ap, [[str(self.jsn.getNearestStations(ip))]])
        return ap

    def askForDate(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.ConfirmationNeut,
                                    Lexicon.OutputNP.AskDate,
                                    Lexicon.OutputNP.Empty)
        return ap

    def dateIsInPast(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionSad,
                                    Lexicon.OutputNP.DateInPast,
                                    Lexicon.OutputNP.AskDate,
                                    Lexicon.OutputNP.Empty)
        return ap

    def askForFlexDate(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.FlexDate,
                                    Lexicon.OutputNP.ConfirmFlex)
        return ap

    def openAnswer(self, ap, ipack):
        # first, if it is the first time, all blanks will be blank
        allBlanks = self.getListOfBlanks(ipack)
        if (len(allBlanks) == 4):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.OutputNP.ExplainOpen,
                                        Lexicon.OutputNP.Open4Blank,
                                        Lexicon.OutputNP.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 3):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.OutputNP.ConfirmationPos,
                                        Lexicon.OutputNP.Open3Blank,
                                        Lexicon.OutputNP.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 2):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.OutputNP.ConfirmationPos,
                                        Lexicon.OutputNP.Open2Blank,
                                        Lexicon.OutputNP.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 1):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.OutputNP.ConfirmationPos,
                                        Lexicon.OutputNP.Open1Blank,
                                        Lexicon.OutputNP.Empty)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        else:
            print("WARN: no or too many blanks!")
            return None

    def getListOfBlanks(self, ipack):
        li = []
        if not ipack.time:
            li.append(Lexicon.OutputNP.Time)
        if ipack.traveller == -1:
            li.append(Lexicon.OutputNP.Traveller)
        if ipack.budget == -1:
            li.append(Lexicon.OutputNP.Budget)
        if ipack.transfers == -1:
            li.append(Lexicon.OutputNP.Transfers)
        return li

    def askForTime(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.AskTime,
                                    Lexicon.OutputNP.Empty)
        return ap

    def askForBudget(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationNeut,
                                    Lexicon.OutputNP.AskBudget,
                                    Lexicon.OutputNP.Empty)
        return ap

    def askForTraveller(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.AskTraveller,
                                    Lexicon.OutputNP.Empty)
        return ap

    def askForTransfers(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.AskTransfers,
                                    Lexicon.OutputNP.Empty)
        return ap

    def explainQuery(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.ExplainQuery,
                                    Lexicon.OutputNP.BePatient)
        return ap

    def petCustomer(self, ap, ip):
        distance = self.jsn.getDistance(ip.origin[0], ip.destination[0])
        if distance == 0:
            return ap
        co2 = computeCO2(distance)
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.PreparePet,
                                    Lexicon.OutputNP.Pet,
                                    Lexicon.OutputNP.Source)
        ap = self.replaceAllCustomStrings(
            ap, co2)
        return ap

    def askForStart(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.OutputNP.Empty,
                                    Lexicon.OutputNP.AskForStart,
                                    Lexicon.OutputNP.Empty)
        return ap

    def sayGoodbye(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.OutputNP.ConfirmationPos,
                                    Lexicon.OutputNP.BestWishes,
                                    Lexicon.OutputNP.GoodBye)
        return ap

    def originAgain(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.OutputNP.OriginAgain,
                                    Lexicon.OutputNP.AskForOrigin,
                                    Lexicon.OutputNP.Empty)
        return ap

from src.Data.Lexicon import Lexicon, ChooseRandomAnswer
from src.Packages.AnswerPackage import AnswerPackage
from src.Worker.Helper import load, computeCO2
import time


class AnswerFormulator:
    @load
    def __init__(self, jsn):
        self.jsn = jsn
        time.sleep(1)

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
                                    Lexicon.Output.FirstGreetings,
                                    Lexicon.Output.ExplGreetings,
                                    Lexicon.Output.QuestGreetings)
        return ap

    def startTutorial(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.TutorialMsg,
                                    Lexicon.Output.AskForUnderstanding)
        return ap

    def moreInformationsToChatbots(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.ConfirmationNeut,
                                    Lexicon.Output.GiveMoreInfosToChatbots,
                                    Lexicon.Output.WikiToChatbots)
        return ap

    def askForOrigin(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationNeut,
                                    Lexicon.Output.AskForOrigin,
                                    Lexicon.Output.Empty)
        return ap

    def confirmOrigin(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.ConfirmationThinking,
                                    Lexicon.Output.AskForConfirmation,
                                    Lexicon.Output.Empty)
        ap = self.replaceAllCustomStrings(
            ap, [ip.origin])
        return ap

    def startAutoCorrectionForOrigin(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationThinking,
                                    Lexicon.Output.ExplainAutocorrection,
                                    Lexicon.Output.AskForCitys)
        return ap

    def askForDestination(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationNeut,
                                    Lexicon.Output.AskForDestination,
                                    Lexicon.Output.Empty)
        return ap

    def confirmDestination(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.ConfirmationThinking,
                                    Lexicon.Output.AskForConfirmation,
                                    Lexicon.Output.Empty)
        ap = self.replaceAllCustomStrings(
            ap, [ip.destination])
        return ap

    def startAutoCorrectionForDestination(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationThinking,
                                    Lexicon.Output.ExplainAutocorrection,
                                    Lexicon.Output.AskForCitys)
        return ap

    def askForFlexibleStartpoint(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.AskFlexibleStartpoint,
                                    Lexicon.Output.FSCookie)
        ap = self.replaceAllCustomStrings(
            ap, [[len(self.jsn.getNearestStations(ip))]])
        return ap

    def showStartPoints(self, ap, ip):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.LookingForInfo,
                                    Lexicon.Output.GiveAllStartpoints,
                                    Lexicon.Output.AskForStartponts)
        ap = self.replaceAllCustomStrings(
            ap, [[str(self.jsn.getNearestStations(ip))]])
        return ap

    def askForDate(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.Output.ConfirmationNeut,
                                    Lexicon.Output.AskDate,
                                    Lexicon.Output.Empty)
        return ap

    def dateIsInPast(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionSad,
                                    Lexicon.Output.DateInPast,
                                    Lexicon.Output.AskDate,
                                    Lexicon.Output.Empty)
        return ap

    def askForFlexDate(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.FlexDate,
                                    Lexicon.Output.ConfirmFlex)
        return ap

    def openAnswer(self, ap, ipack):
        # first, if it is the first time, all blanks will be blank
        allBlanks = self.getListOfBlanks(ipack)
        if (len(allBlanks) == 4):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.Output.ExplainOpen,
                                        Lexicon.Output.Open4Blank,
                                        Lexicon.Output.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 3):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.Output.ConfirmationPos,
                                        Lexicon.Output.Open3Blank,
                                        Lexicon.Output.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 2):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.Output.ConfirmationPos,
                                        Lexicon.Output.Open2Blank,
                                        Lexicon.Output.OpenQuestion)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        elif (len(allBlanks) == 1):
            self.formulateGeneralAnswer(ap,
                                        Lexicon.Internals.EmotionHappy,
                                        Lexicon.Output.ConfirmationPos,
                                        Lexicon.Output.Open1Blank,
                                        Lexicon.Output.Empty)
            ap = self.replaceAllCustomStrings(ap, allBlanks)
            return ap
        else:
            print("WARN: no or too many blanks!")
            return None

    def getListOfBlanks(self, ipack):
        li = []
        if not ipack.time:
            li.append(Lexicon.Output.Time)
        if ipack.traveller == -1:
            li.append(Lexicon.Output.Traveller)
        if ipack.budget == -1:
            li.append(Lexicon.Output.Budget)
        if ipack.transfers == -1:
            li.append(Lexicon.Output.Transfers)
        return li

    def askForTime(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.AskTime,
                                    Lexicon.Output.Empty)
        return ap

    def askForBudget(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationNeut,
                                    Lexicon.Output.AskBudget,
                                    Lexicon.Output.Empty)
        return ap

    def askForTraveller(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.AskTraveller,
                                    Lexicon.Output.Empty)
        return ap

    def askForTransfers(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.AskTransfers,
                                    Lexicon.Output.Empty)
        return ap

    def explainQuery(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.ExplainQuery,
                                    Lexicon.Output.BePatient)
        return ap

    def petCustomer(self, ap, ip):
        distance = self.jsn.getDistance(ip.origin[0], ip.destination[0])
        if distance == 0:
            return ap
        co2 = computeCO2(distance)
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.PreparePet,
                                    Lexicon.Output.Pet,
                                    Lexicon.Output.Source)
        ap = self.replaceAllCustomStrings(
            ap, co2)
        return ap

    def askForStart(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionThoughtful,
                                    Lexicon.Output.Empty,
                                    Lexicon.Output.AskForStart,
                                    Lexicon.Output.Empty)
        return ap

    def sayGoodbye(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionHappy,
                                    Lexicon.Output.ConfirmationPos,
                                    Lexicon.Output.BestWishes,
                                    Lexicon.Output.GoodBye)
        return ap

    def originAgain(self, ap):
        self.formulateGeneralAnswer(ap,
                                    Lexicon.Internals.EmotionWriter,
                                    Lexicon.Output.OriginAgain,
                                    Lexicon.Output.AskForOrigin,
                                    Lexicon.Output.Empty)
        return ap

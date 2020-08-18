from src.Data.Lexicon import Lexicon, ChooseRandomAnswer
from src.Packages.AnswerPackage import AnswerPackage

# the Error Checker just checks if there is some output created
# if the state is repeated, it sets a signal for this in the message
# if something went terrible wrong, it creates an error-message for the user


class ErrorChecker:
    def repareErrors(self, IP, AP):
        if AP is None:
            AP = self.createErrorMessage(AP)
        if IP.repeat:
            IP, AP = self.replaceRepeats(IP, AP)
        if not AP.filled:
            AP = self.putErrorMessage(AP)

        return IP, AP

    def replaceRepeats(self, IP, AP):
        AP.setPreface(ChooseRandomAnswer(Lexicon.Output.NotUnderstand))
        AP.setEmotion(Lexicon.Internals.EmotionSad)
        IP.setRepeat(False)
        print("repetition detected and fixed.")
        return IP, AP

    def createErrorMessage(self, AP):
        AP = AnswerPackage()
        AP = self.putErrorMessage(AP)
        return AP

    def putErrorMessage(self, AP):
        AP.setEmotion(Lexicon.Internals.EmotionSad)
        AP.setPreface(ChooseRandomAnswer(Lexicon.Output.NotUnderstand))
        AP.setFilled(True)
        print("replaced answer")
        return AP

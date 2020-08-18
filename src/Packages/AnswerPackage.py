from src.Packages.Package import Package

# this is the package which contains all the messages created by the NLU
# the front-end unpacks this package and prints its contents to the user


class AnswerPackage(Package):
    def __init__(self):
        # default to none
        self.emotion = None  # string
        self.preface = None  # string
        self.mainAnswer = None  # string
        self.last = None  # string
        self.filled = False  # bool

    def setAll(self, emotion, preface, mainAnswer, last):
        if emotion != "" and type(emotion) is str:
            self.emotion = emotion
        if preface != "" and type(preface) is str:
            self.preface = preface
        if mainAnswer != "" and type(mainAnswer) is str:
            self.mainAnswer = mainAnswer
        if last != "" and type(last) is str:
            self.last = last
        self.setFilled(True)

    def setEmotion(self, emotion):
        if emotion != "" and type(emotion) is str:
            self.emotion = emotion

    def setPreface(self, preface):
        if preface != "" and type(preface) is str:
            self.preface = preface

    def setMainAnswer(self, mainAnswer):
        if mainAnswer != "" and type(mainAnswer) is str:
            self.mainAnswer = mainAnswer

    def setLast(self, last):
        if last != "" and type(last) is str:
            self.last = last

    def setFilled(self, filled):
        self.filled = filled

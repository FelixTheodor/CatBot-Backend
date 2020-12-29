from src.Data.Lexicon import Lexicon
from src.Worker.Helper import load
from datetime import datetime, timedelta
import copy
import re
import numpy as np
import os

# the analyzer is the core of the NLU
# here, the input from the user gets analyzed
# informations that are important for the search are stored
# and the state is updated, depending on the detected informations


class Analyzer:
    @load
    def __init__(self, jsm, config):
        # since the spacy library costs a lot of performance,
        # a smaller version is used for testing
        if config["big_spacy"] == "false":
            # ignore vector warnings since they spam the log
            os.environ['SPACY_WARNING_IGNORE'] = 'W007'
            import spacy
            try:
                self.spacy = spacy.load(
                    '/home/pi/.local/lib/python3.7/site-packages/de_core_news_sm/de_core_news_sm-2.3.0')
            except IOError:
                self.spacy = spacy.load('de_core_news_sm')
        else:
            os.environ['SPACY_WARNING_IGNORE'] = 'W008'  # see above
            import spacy
            try:
                self.spacy = spacy.load(
                    '/home/pi/.local/lib/python3.7/site-packages/de_core_news_md/de_core_news_md-2.3.0')
            except IOError:
                self.spacy = spacy.load('de_core_news_md')
        self.jsn = jsm
        self.allCitys = self.jsn.getAllCityNames()

    # the main method to start the analysis
    # checks the current status and starts the right methods
    def analyze(self, message, ipack):
        # check values from the ipack and set values in the r(eturn)_ipack
        r_ipack = copy.deepcopy(ipack)

        # spacy-analysis
        analyzed_msg = self.spacy(message)
        tokens_msg = [tok.lower_ for tok in analyzed_msg]

        # start the chat
        if message == Lexicon.Internals.StartChat:
            r_ipack.setState(Lexicon.Internals.Y_N_Tutorial)

        # y_n_tutorial
        if ipack.state == Lexicon.Internals.Y_N_Tutorial:
            if self.AnswerMeansYes(tokens_msg):
                r_ipack.setState(Lexicon.Internals.StartTutorial)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Origin)
            else:
                r_ipack.setRepeat(True)

        # start Tutorial
        if ipack.state == Lexicon.Internals.StartTutorial:
            if self.AnswerMeansYes(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Origin)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(
                    Lexicon.Internals.GiveMoreInformationsToChatbots)
            else:
                r_ipack.setRepeat(True)

        # Give More Informations to Chatbot
        if ipack.state == Lexicon.Internals.GiveMoreInformationsToChatbots:
            r_ipack.setState(Lexicon.Internals.Origin)

        # set Origin
        if ipack.state == Lexicon.Internals.Origin or ipack.state == Lexicon.Internals.OriginAgain:
            # find city-strings in the user input
            # fullMatch means, we found the name spelled exactly like the user did
            places, fullMatch = self.tryToGetMatchingCitys(analyzed_msg)

            if len(places) > 0 and fullMatch:
                r_ipack.setOrigin(places)
                r_ipack.setState(Lexicon.Internals.Destination)
            elif len(places) > 0 and not fullMatch:
                # if the spelling of the user wasnt correct, we try to confirm it
                r_ipack.setOrigin(places)
                r_ipack.setState(Lexicon.Internals.Y_N_Origin)
            else:
                r_ipack.setState(Lexicon.Internals.OriginCorrection)

        # confirm Origin
        if ipack.state == Lexicon.Internals.Y_N_Origin:
            if self.AnswerMeansYes(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Destination)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setOrigin([])
                r_ipack.setState(Lexicon.Internals.OriginCorrection)
            else:
                r_ipack.setRepeat(True)

        # on origincorrection, the front-end accepts and sends only existing citys
        if ipack.state == Lexicon.Internals.OriginCorrection:
            r_ipack.setOrigin(message)
            r_ipack.setState(Lexicon.Internals.Destination)

        # set Destination
        if ipack.state == Lexicon.Internals.Destination:
            # find city-strings in the user input
            # fullMatch means, we found the name spelled exactly like the user did
            places, fullMatch = self.tryToGetMatchingCitys(analyzed_msg)

            if len(places) > 0 and fullMatch:
                r_ipack.setDestination(places)
                # find other stations that would make sense as a starting point
                if len(self.jsn.getNearestStations(r_ipack)) != 0:
                    r_ipack.setState(Lexicon.Internals.FlexibleStartPoint)
                else:
                    r_ipack.setState(Lexicon.Internals.Date)
            elif len(places) > 0 and not fullMatch:
                r_ipack.setDestination(places)
                r_ipack.setState(Lexicon.Internals.Y_N_Destination)
            else:
                r_ipack.setState(Lexicon.Internals.DestinationCorrection)

        # confirm Destination
        if ipack.state == Lexicon.Internals.Y_N_Destination:
            if self.AnswerMeansYes(tokens_msg):
                # find other stations that would make sense as a starting point
                if len(self.jsn.getNearestStations(r_ipack)) != 0:
                    r_ipack.setState(Lexicon.Internals.FlexibleStartPoint)
                else:
                    r_ipack.setState(Lexicon.Internals.Date)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setDestination([])
                r_ipack.setState(
                    Lexicon.Internals.DestinationCorrection)
            else:
                r_ipack.setRepeat(True)

        if ipack.state == Lexicon.Internals.DestinationCorrection:
            r_ipack.setDestination(message)
            if len(self.jsn.getNearestStations(r_ipack)) != 0:
                r_ipack.setState(Lexicon.Internals.FlexibleStartPoint)
            else:
                r_ipack.setState(Lexicon.Internals.Date)

        # set Flexible Startpoint if users whishes to
        if ipack.state == Lexicon.Internals.FlexibleStartPoint:
            if self.AnswerIsWhichQuestion(tokens_msg):
                r_ipack.setState(Lexicon.Internals.ShowPossibleStartPoints)
            elif self.AnswerMeansYes(tokens_msg):
                r_ipack.appendOrigin(
                    self.jsn.getNearestStations(r_ipack))
                r_ipack.setState(Lexicon.Internals.Date)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Date)
            else:
                r_ipack.setRepeat(True)

        if ipack.state == Lexicon.Internals.ShowPossibleStartPoints:
            if self.AnswerMeansYes(tokens_msg):
                r_ipack.appendOrigin(
                    self.jsn.getNearestStations(r_ipack))
                r_ipack.setState(Lexicon.Internals.Date)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Date)
            else:
                r_ipack.setRepeat(True)

        # set the Date
        if ipack.state == Lexicon.Internals.Date or ipack.state == Lexicon.Internals.PastDate:
            date, isInPast = self.getDate(message)
            if date:
                if not isInPast:
                    r_ipack.setDate([date])
                    r_ipack.setState(Lexicon.Internals.FlexibleDate)
                else:
                    r_ipack.setState(Lexicon.Internals.PastDate)
            else:
                r_ipack.setRepeat(True)

        # make the date flexible, plus and minus one day
        if ipack.state == Lexicon.Internals.FlexibleDate:
            if self.AnswerMeansYes(tokens_msg):
                self.expandDate(r_ipack)
                r_ipack.setState(Lexicon.Internals.Open)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(Lexicon.Internals.Open)
            else:
                r_ipack.setRepeat(True)

        # in the open state the user can choose to add several parameters
        # or start the query right away
        # everytime the user added another param, the system goes back to the open state
        if ipack.state == Lexicon.Internals.Open:
            # find all possible states
            possNextStates = []

            # if keywords for the state appear, it is added a a next possible state
            if not ipack.time:
                if self.AnswerIsAboutTime(tokens_msg):
                    # compute vector-similarity between keywords of the state and the input
                    sim_time = analyzed_msg.similarity(self.spacy(
                        "".join(Lexicon.Internals.Time)))
                    possNextStates.append([sim_time, Lexicon.Internals.Time])
            if ipack.traveller == -1:
                if self.AnswerIsAboutTraveller(tokens_msg):
                    sim_travel = analyzed_msg.similarity(self.spacy(
                        "".join(Lexicon.Internals.Traveller)))
                    possNextStates.append(
                        [sim_travel, Lexicon.Internals.Traveller])
            if ipack.budget == -1:
                if self.AnswerIsAboutMoney(tokens_msg):
                    sim_money = analyzed_msg.similarity(
                        self.spacy("".join(Lexicon.Analyze.Money)))
                    possNextStates.append(
                        [sim_money, Lexicon.Internals.Budget])
            if ipack.transfers == -1:
                if self.AnswerIsAboutTransfers(tokens_msg):
                    sim_trans = analyzed_msg.similarity(self.spacy(
                        "".join(Lexicon.Analyze.Transfers)))
                    possNextStates.append(
                        [sim_trans, Lexicon.Internals.Transfers])

            # set state depending on the found possible next states
            # only if there are no other indicators, start the query
            if len(possNextStates) == 0:
                if self.AnswerIsAboutSearch(tokens_msg):
                    r_ipack.setState(Lexicon.Internals.Query)
                else:
                    r_ipack.setRepeat(True)
            # if there is only one possible next state, the case is clear
            # this is the ONLY place where the ipack itself is changed, because sometimes
            # the user gives the answer to state within the same message
            elif len(possNextStates) == 1:
                ipack.setState(possNextStates[0][1])
            # if there are multiple, check which word vectors are the closest to the input
            else:
                r_ipack.setState(max(possNextStates)[1])

        # Time
        if ipack.state == Lexicon.Internals.Time:
            # get Time takes the boolean specific state
            # its true if the message is an answer to the traveller state and wrong if not
            timeTo, worked = self.getTime(
                message, tokens_msg, r_ipack.state == Lexicon.Internals.Time)
            if worked:
                r_ipack.setTime(timeTo)
                # if no blank spaces are left, query
                if r_ipack.hasNoBlanks():
                    r_ipack.setState(Lexicon.Internals.Query)
                else:
                    r_ipack.setState(Lexicon.Internals.Open)
            else:
                if r_ipack.state == Lexicon.Internals.Open:
                    r_ipack.setState(Lexicon.Internals.Time)
                else:
                    r_ipack.setRepeat(True)

        # Traveller
        if ipack.state == Lexicon.Internals.Traveller:
            # get Traveller takes the boolean specific state
            # its true if the message is an answer to the traveller state and wrong if not
            traveller, worked = self.getTraveller(
                tokens_msg, r_ipack.state == Lexicon.Internals.Traveller)
            if worked:
                r_ipack.setTraveller(traveller)
                # if no blank spaces are left, query
                if r_ipack.hasNoBlanks():
                    r_ipack.setState(Lexicon.Internals.Query)
                else:
                    r_ipack.setState(Lexicon.Internals.Open)
            else:
                if r_ipack.state == Lexicon.Internals.Open:
                    r_ipack.setState(Lexicon.Internals.Traveller)
                else:
                    r_ipack.setRepeat(True)

        # Budget
        if ipack.state == Lexicon.Internals.Budget:
            budget, worked = self.getBudget(message)
            if worked:
                r_ipack.setBudget(budget)
                # if no blank spaces are left, query
                if r_ipack.hasNoBlanks():
                    r_ipack.setState(Lexicon.Internals.Query)
                else:
                    r_ipack.setState(Lexicon.Internals.Open)
            else:
                if r_ipack.state == Lexicon.Internals.Open:
                    r_ipack.setState(Lexicon.Internals.Budget)
                else:
                    r_ipack.setRepeat(True)

        # Transfers
        if ipack.state == Lexicon.Internals.Transfers:
            transfers, worked = self.getTransfers(
                tokens_msg, r_ipack.state == Lexicon.Internals.Transfers)
            if worked:
                r_ipack.setTransfers(transfers)
                # if no blank spaces are left, query
                if r_ipack.hasNoBlanks():
                    r_ipack.setState(Lexicon.Internals.Query)
                else:
                    r_ipack.setState(Lexicon.Internals.Open)
            else:
                if r_ipack.state == Lexicon.Internals.Open:
                    r_ipack.setState(Lexicon.Internals.Transfers)
                else:
                    r_ipack.setRepeat(True)

        # Query (handled by the RequestManager)
        if ipack.state == Lexicon.Internals.Query:
            r_ipack.setState(Lexicon.Internals.PetCustomer)

        # pet customer
        if ipack.state == Lexicon.Internals.PetCustomer:
            r_ipack.setState(Lexicon.Internals.AskForAnotherStart)

        # here, the user can decide to start the chat again
        if ipack.state == Lexicon.Internals.AskForAnotherStart:
            if self.AnswerMeansYes(tokens_msg):
                r_ipack.fullReset()
                r_ipack.setState(Lexicon.Internals.OriginAgain)
            elif self.AnswerMeansNo(tokens_msg):
                r_ipack.setState(Lexicon.Internals.SayGoodbye)
            else:
                r_ipack.setRepeat(True)

        # if the user said goodybe but the writes something again, ask again for another start
        if ipack.state == Lexicon.Internals.SayGoodbye:
            r_ipack.setState(Lexicon.Internals.AskForAnotherStart)

        return r_ipack

# methods for actual analysis
    # methods to check for simple keyword-matching
    def checkForKeywords(self, msg_toks, keywords):
        for keyword in keywords:
            for tok in msg_toks:
                if keyword in tok:
                    return True
        return False

    def AnswerMeansYes(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Yes)

    def AnswerMeansNo(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.No)

    def AnswerIsWhichQuestion(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Which)

    def AnswerIsAboutTime(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Time)

    def AnswerIsAboutTraveller(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Traveller)

    def AnswerIsAboutMoney(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Money)

    def AnswerIsAboutTransfers(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Transfers)

    def AnswerIsAboutSearch(self, msg):
        return self.checkForKeywords(msg, Lexicon.Analyze.Search)

    # this method tries to match tokens from the analyzed input to citynames
    def tryToGetMatchingCitys(self, msg):
        # first, check for full matches
        origin = []
        for city in self.allCitys:
            for tok in msg:
                if tok.pos_ == "PROPN":
                    if tok.lower_ == city.lower():
                        origin.append(city)

        if len(origin) != 0:
            return origin, True

        # if there is no full match, check fitting POS with Lev-Distance
        for city in self.allCitys:
            l_city = city.lower()
            for tok in msg:
                if (tok.pos_ == "PROPN" or tok.pos_ == "NOUN") and len(l_city) - len(tok.lower_) < 5:
                    levi = self.levenshtein(l_city, tok.lower_)
                    # the length - values are kinda random, but needed for different length of pos
                    if len(tok.lower_) < 5:
                        if levi < 2:
                            origin.append(city)
                    elif len(tok.lower_) < 10:
                        if levi < 3:
                            origin.append(city)
                    elif len(tok.lower_) < 15:
                        if levi < 4:
                            origin.append(city)
                    else:
                        if levi < 5:
                            origin.append(city)

        return origin, False

    # reimplented levenshtein to be sure that we can debug and understand it
    def levenshtein(self, wantSeq, haveSeq):
        size_x = len(wantSeq) + 1
        size_y = len(haveSeq) + 1
        matrix = np.zeros((size_x, size_y))  # Matrix in size of lengths
        for x in range(size_x):
            matrix[x, 0] = x  # fill x-row for empty string
        for y in range(size_y):
            matrix[0, y] = y  # fill y-row for empty string

        for x in range(1, size_x):
            for y in range(1, size_y):
                subwantSeq = wantSeq[0:x]
                subhaveSeq = haveSeq[0:y]
                if subwantSeq[-1] == subhaveSeq[-1]:
                    # insert element of want in have
                    _insertValue = matrix[x - 1, y] + 1
                    # substitution (weightless)
                    _substValue = matrix[x - 1, y - 1]
                    _deleteValue = matrix[x, y - 1] + \
                        1  # delete element in have

                    # get minimal-value
                    matrix[x, y] = min(_deleteValue, _substValue, _insertValue)
                else:
                    # insert element of want in have
                    _insertValue = matrix[x - 1, y] + 1
                    _substValue = matrix[x - 1, y - 1] + 1  # substitution
                    _deleteValue = matrix[x, y - 1] + 1  # delete element

                    # get minimal-value
                    matrix[x, y] = min(_deleteValue, _substValue, _insertValue)

        return (matrix[size_x - 1, size_y - 1])

    # this method extracts a date from the input, eg:
    # 7. Januar, 7.1, 07.01.2020, 7/1
    def getDate(self, msg):
        day = 0
        month = 0
        year = int(datetime.today().strftime("%Y"))  # current year as default

        isInPast = False
        inputString = msg.lower()

        # find the year
        changedYear = False
        yearList = re.findall(r'20[0-9][0-9]', inputString)
        if len(yearList) == 1:
            year = int(yearList[0])
            changedYear = True
        if len(yearList) > 1:
            for str_year in yearList:
                if str_year[0:2] == "20":
                    year = int(str_year)
                    break
            changedYear = True

        # find the Month & Day via Keyword
        months = {"januar": 1, "februar": 2, "märz": 3,
                  "april": 4, "mai": 5, "juni": 6, "juli": 7, "august": 8,
                  "september": 9, "oktober": 10, "november": 11, "dezember": 12}

        for mon in months.keys():
            if mon in inputString:
                month = months.get(mon)
                check = re.findall(r'[0-9][0-9]?\.?\W*' + mon, inputString)
                if len(check) == 1:
                    day = re.findall(r'[0-9][0-9]?', check[0])
                    day = int(day[0])

        # check for Patterns
        pointPattern = re.findall(
            r'[0-9][0-9]?[\.\/\s][0-9][0-9]?', inputString)
        if len(pointPattern) == 1:
            patt = pointPattern[0]
            patt = patt.replace(".", "/").replace(" ", "/").split("/")
            day = int(patt[0])
            month = int(patt[1])
            newYear = re.findall(
                r'[0-9][0-9]?[\.\/\s][0-9][0-9]?[\.\/\s][0-9][0-9]', inputString)
            if len(newYear) == 1 and not changedYear:
                year = newYear[0]
                year = 2000 + int(year[-2:])
                changedYear = True

        # get the current date
        date_format = "%d/%m/%Y"
        cur_date = datetime.today().strftime(date_format)
        # check for "morgen" and "übermorgen"
        if "morgen" in inputString:
            li = cur_date.split("/")
            day = int(li[0])
            month = int(li[1])
            year = int(li[2])
            if "übermorgen" in inputString:
                day += 2
            else:
                day += 1

        date = [day, month, year]

        if day != 0 and month != 0:
            try:
                today = datetime.today().date()
                # if the date is in the past and the year is not explicitly set...
                if self.getPyDateFrom(date) < today:
                    if not changedYear:
                        date[2] += 1  # we should try next year
                        if self.getPyDateFrom(date) < today:
                            isInPast = True
                    else:
                        isInPast = True
                return date, isInPast
            except TypeError:
                return None, False
        else:
            return None, False

    def getPyDateFrom(self, date):
        date_format = "%d/%m/%Y"
        this_date = f"{str(date[0]).zfill(2)}/{str(date[1]).zfill(2)}/{str(date[2])}"
        try:
            date_f = datetime.strptime(this_date, date_format)
            return date_f.date()
        except ValueError:
            return None

    def expandDate(self, ipack):
        date = self.getPyDateFrom(ipack.date[0])
        prev_day = datetime.strftime(
            date - timedelta(1), '%d-%m-%Y').split("-")
        next_day = datetime.strftime(
            date + timedelta(1), '%d-%m-%Y').split("-")
        ipack.expandDate(prev_day, next_day)

    # this method extracts time from the input, eg:
    # 17:30, 7:30, 17.30, 17 Uhr, 9
    # its a little messy, since there are so many ways to express a certain time
    def getTime(self, msg, msg_toks, specificState):
        hour = -1
        minute = 0

        inputString = msg.lower()

        # Check for first Pattern for Point in Time; 17:30
        pit = re.findall(r'[0-9][0-9]?[:\.\s][0-9][0-9]', inputString)

        if len(pit) == 1:
            pit = pit[0].replace(".", ":").replace(" ", "/").split(":")
            hour = int(pit[0])
            minute = int(pit[1])

        # Check for second pattern; 17 Uhr
        pit = re.findall(r'[0-9][0-9]?\W*uhr', inputString)

        # 17 Uhr dreißig
        if len(pit) == 1:
            pit = pit[0].split("uhr")
            hour = int(pit[0])
            if "dreißig" in inputString:
                minute = 30

        # check for single time
        if len(inputString) == 1 or len(inputString) == 2:
            hour = int(inputString)

        # check for written time:
        num, worked = self.getNumber(msg_toks)
        # this check is for cases like "eine bestimmte uhrzeit"
        if worked and (num == 1 and specificState or num != 1) and hour == -1:
            hour = num
            mi, decr = self.getMinutes(msg_toks)
            if mi != -1:
                if decr:
                    hour -= 1
                    if hour == -1:
                        hour = 23
                minute = mi
            # 3 Uhr -> default is 03:00 at night,
            # but if the user explicitly says another daytime, we should change this
            if "abend" in inputString or "nachmittag" in inputString:
                hour += 12

        if hour != -1:
            pit = [hour, minute]
            return pit, True
        else:
            pit = self.checkForDayTime(msg)
            if pit[0] == -1:
                return pit, False
            else:
                return pit, True

    # this method just checks for articulated datetimes in the string
    def checkForDayTime(self, msg):
        if "morgen" in msg:
            if "früh" in msg:
                return [6, 0]
            else:
                return [8, 0]
        if "vormittag" in msg:
            return [10, 0]
        if "nachmittag" in msg:
            if "früh" in msg:
                return [14, 0]
            elif "spät" in msg:
                return [16, 0]
            else:
                return [15, 0]
        if "mittag" in msg:
            return [12, 0]
        if "abend" in msg:
            if "früh" in msg:
                return [18, 0]
            elif "spät" in msg:
                return [20, 0]
            else:
                return [19, 0]
        if "nacht" in msg:
            return [22, 0]

        return [-1, 0]

    # this method tries to extract minutes from written time
    def getMinutes(self, msg_toks):
        minutes = Lexicon.Analyze.Minutes
        for tok in msg_toks:
            if tok in minutes.keys():
                if tok in Lexicon.Analyze.DecreaseHour:
                    if "vor" in msg_toks:
                        return 45, True
                    elif "nach" in msg_toks:
                        return 15, False
                    else:
                        return minutes[tok], True
                else:
                    return minutes[tok], False
        return -1, False

    # this method extracts budget from the input, eg:
    # 300 Euro, 1$, 257000 €
    def getBudget(self, msg):
        budget = -1

        inputString = msg.lower()

        # check for pattern
        budg = re.findall(r'[0-9]+\W*[e,$,€]?', inputString)

        if len(budg) == 1:
            budg = budg[0].replace("e", " ").replace(
                "€", " ").replace("$", " ").split(" ")
            budget = int(budg[0])

        if budget != -1:
            return budget, True
        else:
            return budget, False

    def getTraveller(self, msg_toks, specificState):
        traveller, worked = self.getNumber(msg_toks)
        if worked:
            if "ich" in msg_toks:
                return traveller + 1, True
            else:
                return traveller, True
        else:
            if "ich" in msg_toks and specificState:
                return 1, True
            else:
                return -1, False

    def getTransfers(self, msg_tokens, specificState):
        number, worked = self.getNumber(msg_tokens)
        if worked and (number != 1 or number == 1 and specificState):
            return number, True
        else:
            return -1, False

    # general method to get written numbers from the input
    def getNumber(self, msg_toks):
        numbers = Lexicon.Analyze.Numbers
        for tok in msg_toks:
            for key in numbers.keys():
                if key in tok and abs(len(key) - len(tok)) < 3:
                    return numbers[key], True
        return -1, False

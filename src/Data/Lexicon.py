import random

# Lexicon is the place for strings
# there should be as little as possible other places in the code with strings
# but just calls to lexicon
# so we can rely on the strings matching if necessary & the code gets cleaner


class Lexicon():

    # Output is the place for strings that will be send to the user
    # all strings are in lists,
    # so we can iterate and choose random formulations
    class Output():

        # Confirmation
        ConfirmationPos = ["Wunderbar!", "Super!",
                           "Gerne!", "Perfekt!", "Klasse!", "Toll!", "Sehr gut!"]
        ConfirmationNeut = ["Alles klar!",
                            "Okay.", "Geht klar.", "In Ordnung.", "Gut."]
        ConfirmationThinking = ["Hmm...", "Aha...",
                                "Soso...", "Okay...", "Ööh..."]
        NotUnderstand = [
            "Ich glaube, ich habe dich nicht ganz verstanden. Kannst du das nochmal wiederholen?",
            "Tut mir leid, irgendwie verstehe ich nicht, was du meinst. Denk dran, ich bin nur ein Kater! Formuliere es bitte nochmal möglichst leicht für mich."]
        # Empty - this is never printed but a message to the website to not even create this part of message
        Empty = ["__empty__"]

        # Greetings
        FirstGreetings = ["Hallo!", "Guten Tag!",
                          "Ich wünschen einen famosen Tag!", "Hey!", "Hellooohoo!", "Hi!", "Herzlich Willkommen!"]
        ExplGreetings = [
            "Mein Name ist CatBot und ich bin hier um dir zu helfen, die günstigsten Reise-Verbindung mit Bus oder Bahn für dein nächstes Abenteuer zu finden.\n" +
            "Zur Zeit kann ich nach Reisebussen von FlixBus und Zugverbindungen der Deutschen Bahn suchen und kenne alle größeren Städte in Deutschland."]
        QuestGreetings = ["Brauchst du ein kleines Tutorial?", "Soll ich dir kurz erklären, wie wir uns am besten verständigen können?",
                          "Brauchst du Hilfe im Umgang mit mir? Keine Sorge, normalerweise bin ich pflegeleicht...", "Möchtest du ein kleines CatBot-Tutorial?"]

        # Tutorial
        TutorialMsg = ["Wie der Name CatBot schon sagt bin ich quasi ein ChatBot mit Pfoten und Schnurrhaaren. Das heißt, ich bin ein Computerprogramm, mit dem du schreiben kannst wie mit einem Menschen.\n" +
                       "Also... in der Theorie. In der Praxis bin ich ja nur ein Kater, deswegen kann es sein, dass ich dich nicht immer so gut verstehe.\n" +
                       "Zur Not kannst du aber über den Button oben rechts immer sehen, was ich gerade an Informationen gespeichert habe und diese manuell löschen.\n" +
                       "Ich werde dir jetzt nach und nach Fragen zu deiner Reise stellen und am Ende hoffentlich die beste Reiseverbindung-Verbindung für dich finden!"]

        GiveMoreInfosToChatbots = [
            "Chatbots sind Computerprogramme ,die versuchen, menschliche Kommunikation zu imitieren und.. Ach, lies doch einfach den Wikipedia-Artikel:"]

        WikiToChatbots = ["{https://de.wikipedia.org/wiki/Chatbot}[Wikipedia-Chatbots]"]

        # questions
        AskForUnderstanding = [
            "Alles klar soweit?", "Hast du alles verstanden?", "Sollen wir dann weitermachen?"]

        AskForConfirmation = [
            "Ich bin mir nicht ganz sicher, ob ich dich richtig verstehe. Ich habe die entsprechende Stadt mal aufgeschrieben: ###0###. Stimmt das so?"]

        # AutoCorrection
        ExplainAutocorrection = [
            "Es scheint, dass ich dich nicht ganz verstehe - oder eventuell kenne ich diese Stadt auch gar nicht. Am besten schreibst du mir mal nur den Namen der Stadt, und ich gebe dir Vorschläge, ob ich diese kenne."]

        AskForCitys = ["Du kannst die dann einfach auswählen!", "Wähle dann einfach die richtige aus der Liste.",
                       "Wenn die richtige Stadt erscheint, musst du dann nur noch draufklicken!"]

        # Origin
        AskForOrigin = ["Dann schieß mal los! Von wo möchtest du deine Fahrt beginnen?",
                        "Von wo aus möchtest du losfahren?", "Nenn mir bitte als nächstes die Stadt, von der aus du losfahren möchtest."]

        AskForDestination = ["Und, hast du dir auch schon überlegt, wo es hingehen soll?",
                             "Und wo soll's für dich hingehen?", "So, dann bräuchte ich jetzt noch deinen Zielort:"]

        # FlexibleStartpoint
        AskFlexibleStartpoint = [
            "In deinem Umkreis sind insgesamt ###0### Städte, die du wahrscheinlich recht einfach erreichst - beispielsweise mit einem Studententicket. Soll ich auch überprüfen, ob eine Abfahrt von dort eventuell günstiger ist?"]

        FSCookie = ["Das kann manchmal wirklich sinnvoll sein!",
                    "Teilweise spart das richtig Geld!", "Also, ich fänd das sinnvoll ;)"]

        LookingForInfo = ["Kleinen Moment, das schaue ich kurz nach...", "Das kann ich dir sagen, kleinen Augenblick..."]
        GiveAllStartpoints = ["Also, es sind die folgenden Städte:  ###0###", "Das hier sind die Städte, die für dich leicht erreichbar wären: ###0###"]
        AskForStartponts = ["Soll ich diese dann auch in die Suche aufnehmen?"]
        # Dates
        DateInPast = [
            "Hm, also wenn mein Kalender richtig ist, liegt dieses Datum schon in der Vergangenheit. Kannst du mir die Frage vielleicht nochmal anders beantworten?"]

        AskDate = ["Und wann soll es losgehen?",
                   "Für wann soll ich nach Verbindungen schauen?"]

        FlexDate = ["Also, wenn du das gerne möchtest kann ich auch flexibel nach Verbindungen in den Tagen um dein Startdatum suchen - vielleicht wird es da dadurch ja günstiger?",
                    "Eventuell ist deine Verbindung günstiger, wenn ich auch in den Tagen vor und nach deiner Abreise suche."]
        ConfirmFlex = ["Soll ich das machen?", "Sollen wir das so machen?",
                       "Möchtest du, dass ich das mache?"]

        # Open
        ExplainOpen = [
            "Also, im Grunde habe ich dann jetzt alle Informationen, die ich brauche. Wenn du möchtest kannst du mir allerdings noch ein paar zusätzliche Infos geben, die ich berücksichtigen soll. Falls dir das so reicht, gib mir einfach Bescheid, und ich starte die Suche!"]
        Open4Blank = [
            "Zurzeit gäbe es noch 4 leere Stellen auf meinem Block, und zwar:\n -###0###\n-###2###\n-###1###\n-###3###\n"]
        Open3Blank = [
            "Dann kannst du mir jetzt noch sagen, ###1###, ###2###, oder ###0###"]
        Open2Blank = [
            "Dann bleiben noch die beiden Punkte ###0### und ###1###."]
        Open1Blank = [
            "Jetzt wäre dann der Zeitpunkt um mir mitzuteilen, ###0###, oder wir starten die Suche!"]
        OpenQuestion = [
            "Welche Informationen möchtest du noch spezifizieren? Oder soll ich die Suche starten?",
            "Möchtest du davon noch etwas anpassen - und wenn ja, was? -, oder bist du bereit für die Ergebnisse der Suche?",
            "Was davon soll ich noch berücksichtigen? Oder sind wir schon zur Suche bereit? :)"]
        Time = ["ob du zu einer spezifischen Zeit loswillst",
                "ob ich am besagten Tag nach einer genauen Zeit schauen soll", "willst du zu einer gewissen Tageszeit abfahren?"]
        Traveller = ["ob ich gleich für mehrere Personen nach einer Verbindung schauen soll",
                     "ob du nicht nur allein fährst", "wie viele Leute noch mit dir verreisen"]
        Budget = ["ob du ein gewisses Budget hast",
                  "ob du gerade knapp bei Kasse bist", "wie viel Geld du investieren kannst"]
        Transfers = ["ob du Fahrten mit vielen Umstiegen leid bist",
                     "ob du eine Höchstoleranz was die Anzahl der Umstiege angeht hast", "wie viele Umstiege du maximal haben möchtest"]

        # Time
        AskTime = ["Dann verrate mir mal, wann du losmöchtest. Du kannst mir eine spezifische Uhrzeit oder eine Tageszeit nennen!",
                   "Dann schieß mal los, bist du eher ein Frühaufsteher oder ein Nachtschwärmer? Nenn mir einfach deine Wohlfühl-Abfahrtszeit! :D"]

        # Traveller
        AskTraveller = ["Wie viele Personen fahren denn mit?",
                        "Nach wie vielen Plätzen soll ich Ausschau halten?"]

        # Budget
        AskBudget = ["Wie viel Geld möchtest du denn maximal ausgeben?",
                     "Mit wie viel Budget soll ich planen?"]

        # Transfers
        AskTransfers = ["Wie viele Umstiege wären denn für dich maximal tolerierbar?",
                        "Wie oft willst du höchstens umsteigen?"]

        # Query
        ExplainQuery = ["Dann habe ich jetzt alles was ich brauche und wühle mich mal durch die Datenbank. Die Ergebnisse zeige ich dir, sobald ich sie sortiert habe!",
                        "Alles klar, dann suche ich jetzt mal nach deinen Verbindungen!"]

        BePatient = [
            "Falls du viele Städte und Daten hast, kann die Suche recht umfangreich werden, also keine Sorge, falls ich etwas länger nicht reagiere ;)"]

        # Pet
        PreparePet = [
            "Übrigens, vielleicht interessiert dich ja die CO2-Bilanz für deine aktuelle Reise? Ich habe da mal was ausgerechnet:"]

        Pet = ["Also, wenn du die Strecke mit der Bahn zurücklegst verbrauchst du insgesamt ###0### Kilogramm CO2, mit dem Bus sind es ###1###.\n Nur als Vergleich: Mit einem durchschnittlichem Auto wären es ###2### und mit dem Flugzeug sogar ###3###!\n Krass, wie viel gespart wird, oder? "]

        Source = [
            "Falls dich das Thema noch mehr interessiert, die zugrundeliegende Tabelle für die Berechnung findest du hier: {https://www.umweltbundesamt.de/bild/vergleich-der-durchschnittlichen-emissionen-0}[Umweltbundesamt]"]

        # End-States
        AskForStart = ["So, möchtest du noch eine weitere Suche starten?"]

        BestWishes = [
            "Dann wünsche ich dir eine tolle Zeit und viel Spaß auf der Reise!"]

        GoodBye = ["Bis zum nächsten mal!", "Bis bald!"]

        # Restart
        OriginAgain = [
            "Alles klar, ich habe dann jetzt alle Informationen gelöscht und wir können wieder von vorne starten!"]

    # Internals is for strings with system-intern meaning & processing
    class Internals():

        # Emotions
        EmotionHappy = "happy"
        EmotionSad = "sad"
        EmotionWriter = "writer"
        EmotionThoughtful = "thinking"

        # MessageCalls
        StartChat = "start"  # Initialize_Chat_From_Beginning"

        # RepeatLastState
        RepeatCode = "__r__"

        # all States
        Y_N_Tutorial = "y/n_tutorial"
        StartTutorial = "tutorial"
        GiveMoreInformationsToChatbots = "chatbots"
        Origin = "origin"
        OriginCorrection = "origincorr"
        Y_N_Origin = "y_n_origin"
        Destination = "destination"
        DestinationCorrection = "destinationcorr"
        Y_N_Destination = "y_n_destination"
        FlexibleStartPoint = "flexstart"
        ShowPossibleStartPoints = "showPoss"
        Date = "date"
        PastDate = "pastdate"
        FlexibleDate = "flexdate"
        Open = "open_state"
        Time = "time"
        Traveller = "traveller"
        Budget = "budget"
        Transfers = "transfers"
        Query = "query"
        PetCustomer = "pet"
        AskForAnotherStart = "afat"
        SayGoodbye = "bye"
        OriginAgain = "or-again"

    # Analyze holds strings for the analyzer

    class Analyze:
        # Yes & No
        Yes = ["ja", "yeah", "japp", "jo", "gerne",
               "absolut", "klar", "gern", "okay", "joa", "jau"]
        No = ["nein", "nö", "nope", "nee", "ne", "nicht"]

        Which = ["welch", "was"]

        # Numbers etc
        Numbers = {"ein": 1, "1": 1, "zwei": 2, "2": 2, "drei": 3, "3": 3, "vier": 4, "4": 4,
                   "fünf": 5, "5": 5, "sechs": 6, "6": 6, "sieben": 7, "7": 7, "acht": 8, "8": 8,
                   "neun": 9, "9": 9, "zehn": 10, "10": 10, "elf": 11, "11": 11, "zwölf": 12, "12": 12}

        Minutes = {"halb": 30, "30": 30, "viertel": 15,
                   "fünfzehn": 15, "fünfundvierzig": 45}
        DecreaseHour = ["viertel", "halb"]

        # topics for open
        Time = ["uhr", "zeit", "abfahrt", "reisen",
                "früh", "termin", "morgen", "mittag", "abend"]
        Traveller = ["person", "mitnehm", "wir", "gemeinsam", "fahr",
                     "anzahl", "leute", "reise", "mehr", "zwei", "drei", "dritt", "allein"]
        Transfers = ["umstieg", "umsteig", "stopp",
                     "warten", "halt", "pause", "toleranz"]
        Money = ["geld", "kasse", "budget", "zahlen", "preis", "euro"]
        Search = ["suche", "query", "los", "such",
                  "beginn", "start", "verbindung", "zeigen", "bereit"]


# Method to get a random answer from string-list
def ChooseRandomAnswer(possibleAnswers):
    i = random.randint(0, len(possibleAnswers) - 1)

    return possibleAnswers[i]

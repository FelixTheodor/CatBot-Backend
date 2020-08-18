import json
from src.Manager.JSONManager import JSONManager
from src.Packages.InformationPackage import InformationPackage
from src.Manager.DialogManager import DialogManager


def testNLU():
    return json.dumps({"Test": "What a test, man"})


def testJSONExtractor(jsondic, jsm):
    jTest = jsm.convertJSONToIPack(jsondic)
    if type(jTest) is InformationPackage:
        return True
    else:
        return False


def testDialogManager(jsondic):
    DM = DialogManager()
    return DM.processRequest(jsondic)

from src.Manager.RequestManager import RequestManager
from src.Packages.InformationPackage import InformationPackage


def testRequest():
    ipack = InformationPackage()
    ipack.setOrigin("Oberhausen")
    ipack.setDestination("München")
    ipack.setDate([[9, 8, 2020]])
    ipack.setTraveller(1)
    ipack.setTime([])
    ipack.setBudget(-1)
    ipack.setTransfers(-1)

    man = RequestManager()
    man.setFromIpack(ipack)

    res = man.makeRequest()
    print(res)


testRequest()

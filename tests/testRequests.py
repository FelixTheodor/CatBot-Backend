from src.Manager.RequestManager import RequestManager
from src.Packages.InformationPackage import InformationPackage
import unittest
import time


class MyRequestTests(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def testRequest(self):
        ipack = InformationPackage()
        ipack.setOrigin("Bochum")
        ipack.setDestination("Dortmund")
        ipack.setDate([[22, 8, 2020]])

        man = RequestManager()
        man.setFromIpack(ipack)

        res = man.makeRequest()
        self.assertTrue("origin" in res)

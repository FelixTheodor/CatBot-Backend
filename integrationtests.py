from tests.testNLPAnswerer import MyAnswerTests
from tests.testNLPAnalyzer import MyAnalyzeTests
from tests.testRequests import MyRequestTests
import unittest

print("\n########################################################")
print("########################Analyzer########################")
print("########################################################")
suite = unittest.TestLoader().loadTestsFromTestCase(MyAnalyzeTests)
unittest.TextTestRunner(verbosity=0).run(suite)
print("########################################################")
print("########################Answerer########################")
print("########################################################")
suite = unittest.TestLoader().loadTestsFromTestCase(MyAnswerTests)
unittest.TextTestRunner(verbosity=0).run(suite)
print("########################################################")
print("########################Requester#######################")
print("########################################################")
suite = unittest.TestLoader().loadTestsFromTestCase(MyRequestTests)
unittest.TextTestRunner(verbosity=0).run(suite)

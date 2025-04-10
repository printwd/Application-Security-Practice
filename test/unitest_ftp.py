import os
import sys
import unittest

import config

from test.ftp.testMain import testMain
from test.ftp.testFTPCommandClient import TestFTPCommandClient

from test.ftp.testSecureMain import testSecureMain

def test_ftp():
    test_main = unittest.TestLoader().loadTestsFromTestCase(testMain)
    test_ftp_command_client = unittest.TestLoader().loadTestsFromTestCase(TestFTPCommandClient)
    
    test_secure_main = unittest.TestLoader().loadTestsFromTestCase(testSecureMain)

    allTests = unittest.TestSuite()
    
    allTests.addTest(test_main)
    allTests.addTest(test_ftp_command_client)
    allTests.addTest(test_secure_main)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)

test_ftp()
import os
import sys
import unittest

import config

from test.db.testMariaDBClient import testMariaDBClient

def test_ftp():
    test_mariadb_client = unittest.TestLoader().loadTestsFromTestCase(testMariaDBClient)
    # test_ftp_command_client = unittest.TestLoader().loadTestsFromTestCase(TestFTPCommandClient)

    allTests = unittest.TestSuite()
    
    allTests.addTest(test_mariadb_client)
    # allTests.addTest(test_ftp_command_client)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)

test_ftp()
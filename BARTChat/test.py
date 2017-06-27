# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import unittest
import sys
sys.path.append('/Users/mu.qiao/workspace/personalproj/playground/BARTChat/')
from bartxml import BARTXml

class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def testBARTavaiablility(self):
        system_not_avaiable_xml = '<?xml version="1.0" encoding="utf-8"?><root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/26/2017</date>\n<time>01:31:46 PM PDT</time>\n<station><name>Richmond</name><abbr>RICH</abbr><message><error>Updates are temporarily unavailable.</error></message></station><message></message></root>'
        BARTdata = BARTXml(system_not_avaiable_xml)
        self.assertFalse(BARTdata.determine_BART_system_availibility())

if __name__ == '__main__':
    unittest.main()

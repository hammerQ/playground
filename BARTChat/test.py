# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import unittest
import sys
sys.path.append('/Users/mu.qiao/workspace/personalproj/playground/BARTChat/')
from bartxml import BARTXml
from lxml import etree

class BartXMLTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def testBARTavaiablility_unavaiable(self):
        system_not_avaiable_xml = '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/26/2017</date><time>01:31:46 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><message><error>Updates are temporarily unavailable.</error></message></station><message></message></root>'
        BARTdata = BARTXml(system_not_avaiable_xml)
        BARTdata.determine_BART_system_availibility()
        self.assertFalse(BARTdata.get_is_BART_avail())

    def testXMLParsingWithlxml(self):
        samplexml = "<root>data</root>"
        xmlroot = etree.fromstring(samplexml)
        self.assertEqual(xmlroot.tag, "root", "not equal")
        self.assertEqual(xmlroot.text, "data", "text not equal")

    def testBARTavaiablility_avaiable(self):
        system_avaiable_xml = '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/27/2017</date><time>03:38:31 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><etd><destination>Fremont</destination><abbreviation>FRMT</abbreviation><limited>0</limited><estimate><minutes>10</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>25</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>40</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate></etd><etd><destination>Millbrae</destination><abbreviation>MLBR</abbreviation><limited>0</limited><estimate><minutes>3</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>18</minutes><platform>2</platform><direction>South</direction><length>9</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>33</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate></etd></station><message></message></root>'
        BARTdata = BARTXml(system_avaiable_xml)
        self.assertTrue(BARTdata.get_is_BART_avail())


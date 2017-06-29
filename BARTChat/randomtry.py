# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import untangle
from lxml import etree

testxml = '<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238456</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[Abc]]></Content><MsgId>6172892165281362744</MsgId></xml>'
xml = '<?xml version="1.0"?><root><child name="child1"/></root>'
unavialbexml = '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/26/2017</date><time>01:31:46 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><message><error>Updates are temporarily unavailable.</error></message></station><message></message></root>'
system_avaiable_xml = '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/27/2017</date><time>03:38:31 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><etd><destination>Fremont</destination><abbreviation>FRMT</abbreviation><limited>0</limited><estimate><minutes>10</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>25</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>40</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate></etd><etd><destination>Millbrae</destination><abbreviation>MLBR</abbreviation><limited>0</limited><estimate><minutes>3</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>18</minutes><platform>2</platform><direction>South</direction><length>9</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>33</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate></etd></station><message></message></root>'
another_xml= '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/27/2017</date><time>03:38:31 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><etd><destination>Fremont</destination><abbreviation>FRMT</abbreviation><limited>0</limited><estimate><minutes>10</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>25</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>40</minutes><platform>2</platform><direction>South</direction><length>6</length><color>ORANGE</color><hexcolor>#ff9933</hexcolor><bikeflag>1</bikeflag></estimate></etd><etd><destination>Millbrae</destination><abbreviation>MLBR</abbreviation><limited>0</limited><estimate><minutes>3</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>18</minutes><platform>2</platform><direction>South</direction><length>9</length><color>RED</color><hexcolor>#ff0000</hexcolor><bikeflag>1</bikeflag></estimate><estimate><minutes>33</minutes><platform>2</platform><direction>South</direction><length>10</length><color>RED</color><error>#ff0000</error><bikeflag>1</bikeflag></estimate></etd></station><message></message></root>'

root_unavailable = etree.fromstring(another_xml)

# print(etree.tostring(root))
# print(etree.tostring(root, pretty_print=True))

print("unavaiable:\n")
for element in root_unavailable.iter():
    print("\ttag is %s - text is %s" % (element.tag, element.text))

for element in root_unavailable.iter("error"):
    print("\tFound error tag is %s - text is %s" % (element.tag, element.text))

print(len(root_unavailable.findall("error")))

for element in root_unavailable.iter("error"):
    if element.text == 'Updates are temporarily unavailable.':
        is_temp_unavail = True
        print("found error with right text")
    else:
        print("other error detected in BART response xml: " + element.text)
        is_temp_unavail = True

print(is_temp_unavail)

# print("\navaiable:\n")
# root_anvaiable = etree.fromstring(system_avaiable_xml)
# for element in root_anvaiable.iter():
#     print("\ttag is %s - text is %s" % (element.tag, element.text))
#
# print("break\n")
# for element in root_anvaiable.iter("error"):
#     print("\tFound error tag is %s - text is %s" % (element.tag, element.text))
# print("break\n")
#
# print(len(root_anvaiable.findall("error")))
#
# if len(root_anvaiable.findall("error")):
#     for element in root_anvaiable.iter("error"):
#         if element.text == 'Updates are temporarily unavailable.':
#             is_temp_unavail = True
#             print("found error with right text")
#         else:
#             print("other error detected in BART response xml: " + element.text)
#             is_temp_unavail = True
# else:
#     print("\tthere is no error")
#     is_temp_unavail = False
# print(is_temp_unavail)

# for child in root:
#     print("Child is " + child.tag + " has child? " + str(len(child)))
#     if len(child):
#         for nestedchild in child:
#             print("\tnestedchild is " + nestedchild.tag + " has child? " + str(len(nestedchild)))
#             if len(nestedchild):
#                 for nested2deepchild in nestedchild:
#                     print("\t\tnested2deepchild is " + nested2deepchild.tag + " has child? " + str(len(nested2deepchild))
#                         + " with text " + nested2deepchild.text)

# obj = untangle.parse(xml)
# print("JSON is " + obj.root.child['name']) # 'child1'
# print("JSON is " + obj.root.child) # 'child1'
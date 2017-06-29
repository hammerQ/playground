# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import untangle
from lxml import etree

testxml = '<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238456</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[Abc]]></Content><MsgId>6172892165281362744</MsgId></xml>'
xml = '<?xml version="1.0"?><root><child name="child1"/></root>'
unavialbexml = '<root><uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH]]></uri><date>06/26/2017</date><time>01:31:46 PM PDT</time><station><name>Richmond</name><abbr>RICH</abbr><message><error>Updates are temporarily unavailable.</error></message></station><message></message></root>'

root = etree.fromstring(unavialbexml)
# print(etree.tostring(root))
print(etree.tostring(root, pretty_print=True))

for element in root.iter():
    print("tag is %s - text is %s" % (element.tag, element.text))

print("break\n")
for element in root.iter("error"):
    print("tag is %s - text is %s" % (element.tag, element.text))
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
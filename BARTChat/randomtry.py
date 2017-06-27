# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import untangle
from lxml import etree

testxml = '<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238456</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[Abc]]></Content><MsgId>6172892165281362744</MsgId></xml>'
xml = '<?xml version="1.0"?><root><child name="child1"/></root>'

root = etree.fromstring(testxml)
print(root.tag)
print(etree.tostring(root))
# obj = untangle.parse(xml)
# print("JSON is " + obj.root.child['name']) # 'child1'
# print("JSON is " + obj.root.child) # 'child1'
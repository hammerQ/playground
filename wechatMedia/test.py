# This Python file uses the following encoding: utf-8
# encoding: utf-8

__author__ = 'mqiao'

import unittest
from wechatxml import WechatXml
from wechatimgdb import Wechat_Database
from wechatimgstorage import WechatStorage
import properties


class TestWeChatImg(unittest.TestCase):

    image_xml = "<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA" \
                "[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238651</CreateTime><MsgType><!" \
                "[CDATA[image]]></MsgType><PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz/cLlBJpiaAdZM4UHb7WWEr04ibLypaMSTIS6XLw6KEFzfcmzOgjnJBicXyTmibQ2XFGY3a8QTw2yfxpibm27RgSh6NcA/0]]>" \
                "</PicUrl><MsgId>6172893002799985471</MsgId><MediaId><![CDATA[edyhcyvwg4Rvv2jLKkHylFvbFVnBXIxdBmdQQuFF3vT2WNKLXgiEmAT1EpsHBJlk]]>" \
                "</MediaId></xml>"
    msg_xml = "<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]>" \
              "</FromUserName><CreateTime>1437248779</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[好天气]]>" \
              "</Content><MsgId>6172936502228759499</MsgId></xml>"
    image_info_dict = dict([('wechatimg_id', 'gh_bf693268132e'), ('fromuser_id', 'oMwf3s4hyHHp1eKxyyiCpb8is9oQ'),
                                     ('create_time', '1437238651'), ('picture_url', 'http://mmbiz.qpic.cn/mmbiz/cLlBJpiaAdZM4UHb7WWEr04ibLypaMSTIS6XLw6KEFzfcmzOgjnJBicXyTmibQ2XFGY3a8QTw2yfxpibm27RgSh6NcA/0'),
                                     ('message_id', '6172893002799985471'),
                                     ('media_id', 'edyhcyvwg4Rvv2jLKkHylFvbFVnBXIxdBmdQQuFF3vT2WNKLXgiEmAT1EpsHBJlk'),
                                     ('message_type', 'image')])
    sample_image_url = 'http://mmbiz.qpic.cn/mmbiz/cLlBJpiaAdZM4UHb7WWEr04ibLypaMSTIS6XLw6KEFzfcmzOgjnJBicXyTmibQ2XFGY3a8QTw2yfxpibm27RgSh6NcA/0'

    def test_determine_media_type_msg_with_imagexml(self):
        wechatdata = WechatXml(self.image_xml)
        wechatdata.determine_media_type()
        self.assertTrue(wechatdata.is_image)
        self.assertFalse(wechatdata.is_video)
        self.assertFalse(wechatdata.is_msg)

    def test_wechat_xml_init(self):
        wechatdata = WechatXml(self.image_xml)
        self.assertFalse(wechatdata.is_image)
        self.assertFalse(wechatdata.is_video)
        self.assertFalse(wechatdata.is_msg)

    def test_determine_media_type_msg_with_msgxml(self):
        wechatdata = WechatXml(self.msg_xml)
        wechatdata.determine_media_type()
        self.assertFalse(wechatdata.is_image)
        self.assertFalse(wechatdata.is_video)
        self.assertTrue(wechatdata.is_msg)

    def test_parse_image_xml(self):
        wechatdata = WechatXml(self.image_xml)
        wechatdata.parse_image_xml()
        expected_value = self.image_info_dict
        self.assertEquals(expected_value, wechatdata.xlm_content_dict)

    def test_parse_msg_xml(self):
        wechatdata = WechatXml(self.msg_xml)
        wechatdata.parse_msg_xml()
        expected_value = dict([('wechatimg_id', 'gh_bf693268132e'), ('fromuser_id', 'oMwf3s4hyHHp1eKxyyiCpb8is9oQ'),
                                    ('create_time', '1437248779'), ('message_id', '6172936502228759499'),
                                    ('content', u'好天气'), ('message_type', 'text')])
        self.assertEquals(expected_value, wechatdata.xlm_content_dict)

    def test_wechatdb_init(self):
        wechatdb = Wechat_Database(self.image_info_dict)
        self.assertEquals(wechatdb.info_dict, self.image_info_dict)
        self.assertTrue(wechatdb.is_local_db_host)

    def test_wechatdb_set_isLocaldbHost(self):
        wechatdb = Wechat_Database(self.image_info_dict)
        self.assertTrue(wechatdb.is_local_db_host)
        wechatdb.set_islocaldbhost(False)
        self.assertFalse(wechatdb.is_local_db_host)

    def test_wechatdb_set_isLocalStorage(self):
        wechatdb = Wechat_Database(self.image_info_dict)
        self.assertTrue(wechatdb.is_local_storage)
        wechatdb.set_islocalstorage(False)
        self.assertFalse(wechatdb.is_local_storage)

    def test_construct_mysql_script_4_insert_img_table(self):
        wechatdb = Wechat_Database(self.image_info_dict)
        wechatdb.construct_mysql_script_4_insert_img_table('image', self.image_xml)
        expected_script = "INSERT INTO image VALUES ('edyhcyvwg4Rvv2jLKkHylFvbFVnBXIxdBmdQQuFF3vT2WNKLXgiEmAT1EpsHBJlk','http://mmbiz.qpic.cn/mmbiz/cLlBJpiaAdZM4UHb7WWEr04ibLypaMSTIS6XLw6KEFzfcmzOgjnJBicXyTmibQ2XFGY3a8QTw2yfxpibm27RgSh6NcA/0','oMwf3s4hyHHp1eKxyyiCpb8is9oQ','<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName><![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238651</CreateTime><MsgType><![CDATA[image]]></MsgType><PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz/cLlBJpiaAdZM4UHb7WWEr04ibLypaMSTIS6XLw6KEFzfcmzOgjnJBicXyTmibQ2XFGY3a8QTw2yfxpibm27RgSh6NcA/0]]></PicUrl><MsgId>6172893002799985471</MsgId><MediaId><![CDATA[edyhcyvwg4Rvv2jLKkHylFvbFVnBXIxdBmdQQuFF3vT2WNKLXgiEmAT1EpsHBJlk]]></MediaId></xml>','comments',NULL,'2015-07-18 12:57:31',NOW());"
        self.assertEquals(expected_script, wechatdb.mysql_script)

    def test_determine_db_properties_islocalhost(self):
        wechatdb = Wechat_Database(self.image_info_dict)
        wechatdb.set_islocaldbhost(True)
        wechatdb.determine_db_properties()
        self.assertEquals(wechatdb.db_host_master, properties.DatabaseProperty.local_host)
        self.assertEquals(wechatdb.db_name, properties.DatabaseProperty.local_db_name)
        self.assertEquals(wechatdb.port, properties.DatabaseProperty.local_port)
        self.assertEquals(wechatdb.user, properties.DatabaseProperty.local_user)
        self.assertEquals(wechatdb.pwd, properties.DatabaseProperty.local_pwd)
        self.assertEquals(wechatdb.timeout, properties.DatabaseProperty.local_timeout)

    def test_obtain_url_4_image_storage(self):
        wechatdb = Wechat_Database(self.image_info_dict)

        self.assertEquals(self.sample_image_url,
                          wechatdb.obtain_url_4_storage())

    def test_wechatimagestorage_setislocalstorage(self):
        storage = WechatStorage(self.sample_image_url)
        storage.set_islocalstorage(True)
        self.assertTrue(storage.is_local_storage)
        storage.set_islocalstorage(False)
        self.assertFalse(storage.is_local_storage)

    def test_wechatimagestorage_init(self):
        storage = WechatStorage(self.sample_image_url)
        self.assertEquals(properties.StorageProperty.remote_storage_domain_name, storage.storage_domain_name)
        storage.set_islocalstorage(True)
        storage.store_image()


if __name__ == '__main__':
    unittest.main()
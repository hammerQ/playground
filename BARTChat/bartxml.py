# This Python file uses the following encoding: utf-8
# encoding: utf-8

import logging
from lxml import etree
__author__ = 'mqiao'

# tags in xml
MEDIA_ID = "MediaId"
PIC_URL = "PicUrl"
MSG_TYPE = "MsgType"
MSG_ID = "MsgId"
CREATE_TIME = "CreateTime"
CONTENT = "Content"
FROM_USER_NAME = "FromUserName"
TO_USER_NAME = "ToUserName"

STATION = 'station'
MESSAGE = 'message'
ERROR = 'error'



class BARTXml ():

    is_temp_unavail = False

    xlm_content_dict = dict()

    def __init__(self, xml):
        self.xml = xml
        is_temp_unavail= False

    def get_is_temp_unavail(self):
        return self.is_temp_unavail

    def determine_BART_system_availibility(self):
        """
        Determine if BART system is available or not
        """
        try:
            xml_received = etree.fromstring(self.xml)
            self.is_temp_unavail = xml_received.findtext(ERROR)
            if self.is_temp_unavail is None:
                self.is_temp_unavail = False
            else:
                self.is_temp_unavail = True
        except:
            logging.info("Error in parsing incoming xml: " + self.xml)
            self.is_temp_unavail = True

    def parse_xml(self):
        """ parse BART API response xml when system is available
        """
        # TODO: figure out a better way to do xml parsing
        try:
            xml_recv_root = etree.fromstring(self.xml)
            wechatimg_id = xml_recv_root.find(TO_USER_NAME).text
            fromuser_id = xml_recv_root.find(FROM_USER_NAME).text
            content = xml_recv_root.find(CONTENT).text
            create_time = xml_recv_root.find(CREATE_TIME).text
            message_id = xml_recv_root.find(MSG_ID).text
            message_type = xml_recv_root.find(MSG_TYPE).text
        except:
            logging.error("Error in parshing incoming XML: " + self.xml)

        self.xlm_content_dict = dict([('wechatimg_id', wechatimg_id), ('fromuser_id', fromuser_id),
                                      ('create_time', create_time), ('message_id', message_id),
                                      ('message_type', message_type), ('content', content)])

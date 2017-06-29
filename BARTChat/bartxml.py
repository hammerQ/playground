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

    xlm_content_dict = dict()

    def __init__(self, xml):
        self.xml = xml
        self.is_BART_system_available = True

    def get_is_BART_avail(self):
        return self.is_BART_system_available

    def determine_BART_system_availibility(self):
        """
        Determine if BART system is available or not
        """
        error_counts = 0
        try:
            xml_received = etree.fromstring(self.xml)
            for element in xml_received.iter("error"):
                error_counts += 1
                if element.text == 'Updates are temporarily unavailable.':
                    self.is_BART_system_available = False
                else:
                    logging.info("other error detected in BART response xml: " + element.text)
                    self.is_BART_system_available = False
        except:
            logging.info("Error in parsing incoming xml: " + self.xml)
            self.is_BART_system_available = False

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

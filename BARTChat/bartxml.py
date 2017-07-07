# This Python file uses the following encoding: utf-8
# encoding: utf-8

import logging
from lxml import etree

BART_ERROR_MSG = 'Updates are temporarily unavailable.'
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

    def get_is_bart_avail(self):
        return self.is_BART_system_available

    def determine_bart_system_availibility(self):
        """
        Determine if BART system is available or not
        """
        try:
            xml_received = etree.fromstring(self.xml)
            for element in xml_received.iter(ERROR):
                if element.text == BART_ERROR_MSG:
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
        try:
            xml_recv_root = etree.fromstring(self.xml)
            station_name_element = xml_recv_root.find('station/name')
            logging.info("station Name tag: " + station_name_element.tag)
            logging.info("Station Name text: " + station_name_element.text)

            if type(station_name_element) is None:
                logging.error("None station name in return BART xml" + self.xml)
                station_name_str = "None"
            else:
                station_name_str = station_name_element.text  # there should be just one station
            # station_name_abbr_str = xml_recv_root.findall('station/abbr').text


        except:
            logging.error("Error in parshing incoming XML: " + self.xml)
            station_name_str = "None"

        self.xlm_content_dict = dict([('station_name', station_name_str)])
        # self.xlm_content_dict = dict([('station_name', station_name_str), ('station_name_abbr', station_name_abbr_str)])
        return self.xlm_content_dict
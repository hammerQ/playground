# This Python file uses the following encoding: utf-8
# encoding: utf-8

import logging
from .bartxml import BARTXml


class BARTXMLProcessor:

    def process_xml_posted(xml):
        """
        Based on posted xml, construct the corresponding response
        :param xml: posted xml from BART open API server
        :return: dictionary of incoming request
        """

        BARTdata = BARTXml(xml)
        is_avaiable = BARTdata.determine_BART_system_availibility()

        if is_avaiable:
            logging.info("\tReceived xml contains image")
            BARTdata.parse_xml()
            return BARTdata.xlm_content_dict
        else:
            logging.error("\tBART API is temporarily unavailable")
            return None

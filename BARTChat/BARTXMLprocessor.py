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
        BARTdata.determine_media_type()

        if BARTdata.is_image:
            logging.info("\tReceived xml contains image")
            BARTdata.parse_image_xml()
        elif BARTdata.is_msg:
            logging.info("\tReceived xml contains msg")
            BARTdata.parse_msg_xml()

        elif BARTdata.is_video:
            logging.info("\tReceived xml contains video")
            BARTdata.parse_video_xml()

        else:
            logging.error("\tReceived other types of xml")
            return None
        return BARTdata.xlm_content_dict
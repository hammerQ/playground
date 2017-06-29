# This Python file uses the following encoding: utf-8
# encoding: utf-8

import logging

from Tools.wechatxml import WechatXml


class WechatXMLProcessor:

    def process_xml_posted(xml):
        """
        Based on posted xml, construct the corresponding response
        :param xml: posted xml from WeChat server
        :return: dictionary of incoming request
        """

        wechatdata = WechatXml(xml)
        wechatdata.determine_media_type()

        if wechatdata.is_image:
            logging.info("\tReceived xml contains image")
            wechatdata.parse_image_xml()
        elif wechatdata.is_msg:
            logging.info("\tReceived xml contains msg")
            wechatdata.parse_msg_xml()

        elif wechatdata.is_video:
            logging.info("\tReceived xml contains video")
            wechatdata.parse_video_xml()

        else:
            logging.error("\tReceived other types of xml")
            return None
        return wechatdata.xlm_content_dict
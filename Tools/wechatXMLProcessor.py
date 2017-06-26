# This Python file uses the following encoding: utf-8
# encoding: utf-8

import logging
from wechatxml import WechatXml


class WechatXMLProcessor ():

    def process_xml_posted(xml):
        """
        Based on posted xml, construct the corresponding response
        :param xml: posted xml from WeChat server
        :return: respond body
        """

        wechatdata = WechatXml(xml)
        wechatdata.determine_media_type()
        # TODO: to extend to other types of media type
        if wechatdata.is_image:
            logging.info("\tReceived xml contains image")
            wechatdata.parse_image_xml()
            # store image content and info into storage and db
            wechatdb = Wechat_Database(wechatdata)
            wechatdb.store_media_info_to_db(xml)
            msg_info = wechatdata.xlm_content_dict
        elif wechatdata.is_msg:
            logging.info("\tReceived xml contains msg")
            wechatdata.parse_msg_xml()
            msg_info = wechatdata.xlm_content_dict
            if is_request_image_back(msg_info):
            # send image back. right now just a message
                logging.info("\tRecieved xml request: asking for photos")
                wechatdata.is_request = True
                downloader = RequestProcessor(msg_info)
                callback_msg_content = downloader.uploadAllPhotosOfUser()
                msg_info['content'] = callback_msg_content
        elif wechatdata.is_video:
            logging.info("\tReceived xml contains video")
            # store video content and info into storage and db
            wechatdata.parse_video_xml()
            wechatdb = Wechat_Database(wechatdata)
            wechatdb.store_media_info_to_db(xml)
            msg_info = wechatdata.xlm_content_dict
        else:
            logging.info("\tReceived other types of xml")

        #TODO get the reture obj figured out
        return "something"
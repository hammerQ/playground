# This Python file uses the following encoding: utf-8
# encoding: utf-8

# tags in xml
MEDIA_ID = "MediaId"
PIC_URL = "PicUrl"
MSG_TYPE = "MsgType"
MSG_ID = "MsgId"
CREATE_TIME = "CreateTime"
CONTENT = "Content"
FROM_USER_NAME = "FromUserName"
TO_USER_NAME = "ToUserName"

__author__ = 'mqiao'
import xml.etree.ElementTree as element_tree
import logging


class WechatXml ():

    is_image = False
    is_msg = False
    is_video = False
    is_request = False
    xlm_content_dict = dict()


    def __init__(self, xml):
        self.xml = xml
        self.is_image = False
        self.is_msg = False
        self.is_video = False
        self.is_request = False

    def set_isImageTrue(self):
        self.is_msg = False
        self.is_image = True
        self.is_video = False

    def set_isTextTrue(self):
        self.is_msg = True
        self.is_image = False
        self.is_video = False

    def set_isVideoTrue(self):
        self.is_msg = False
        self.is_image = False
        self.is_video = True

    def determine_media_type(self):
        """
        Determine if posted XML is for image or not and set the flag accordingly
        """
        try:
            xml_received = element_tree.fromstring(self.xml)
            message_type = xml_received.find("MsgType").text
            if message_type == 'image':
                self.set_isImageTrue()
            elif message_type == 'text':    #request is a special type of text/msg
                self.set_isTextTrue()
            elif message_type == 'video':
                self.set_isVideoTrue()
            else:
                logging.error("un-recognized media format " + message_type)
                self.is_msg = False
        except:
            logging.error("Error in parshing incoming xml: " + self.xml)

    def parse_image_xml(self):
        """ parse WeChat picture xml
        """
        try:
            xml_received = element_tree.fromstring(self.xml)
            wechatimg_id = xml_received.find(TO_USER_NAME).text
            fromuser_id = xml_received.find(FROM_USER_NAME).text
            create_time = xml_received.find(CREATE_TIME).text
            message_type = xml_received.find(MSG_TYPE).text
            picture_url = xml_received.find(PIC_URL).text
            message_id = xml_received.find(MSG_ID).text
            media_id = xml_received.find(MEDIA_ID).text
            logging.info("received picture: "+picture_url)
            self.xlm_content_dict = dict([('wechatimg_id', wechatimg_id), ('fromuser_id', fromuser_id),
                                     ('create_time', create_time), ('picture_url', picture_url), ('message_id', message_id),
                                     ('media_id', media_id), ('message_type', message_type)])
        except:
            logging.error("Error in parshing incoming XML: " + self.xml)

    def parse_msg_xml(self):
        """ parse WeChat msg xml
        """
        try:
            xml_recv = element_tree.fromstring(self.xml)
            wechatimg_id = xml_recv.find(TO_USER_NAME).text
            fromuser_id = xml_recv.find(FROM_USER_NAME).text
            content = xml_recv.find(CONTENT).text
            create_time = xml_recv.find(CREATE_TIME).text
            message_id = xml_recv.find(MSG_ID).text
            message_type = xml_recv.find(MSG_TYPE).text
        except:
            logging.error("Error in parshing incoming XML: " + self.xml)

        self.xlm_content_dict = dict([('wechatimg_id', wechatimg_id), ('fromuser_id', fromuser_id),
                                      ('create_time', create_time), ('message_id', message_id),
                                      ('message_type', message_type), ('content', content)])

    def parse_video_xml(self):
        """ parse WeChat video xml
        """
        try:
            xml_recv = element_tree.fromstring(self.xml)
            wechatimg_id = xml_recv.find(TO_USER_NAME).text
            fromuser_id = xml_recv.find(FROM_USER_NAME).text
            create_time = xml_recv.find(CREATE_TIME).text
            message_type = xml_recv.find(MSG_TYPE).text  # should be "video"
            media_id = xml_recv.find(MEDIA_ID).text # used to pull down video data
            video_thumb = xml_recv.find("ThumbMediaId").text    # thumbnail for the video

        except:
            logging.error("Error in parsing incoming XML: " + self.xml)

        self.xlm_content_dict = dict([('wechatimg_id', wechatimg_id), ('fromuser_id', fromuser_id),
                                      ('create_time', create_time), ('video_thumb', video_thumb),
                                      ('message_type', message_type), ('media_id', media_id)])
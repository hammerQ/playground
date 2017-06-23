# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'
import logging
from flask import Flask, request, json, make_response
import hashlib
import time
import MySQLdb as mdb
import properties as service_prop
from properties import ConstantValues
from wechatxml import WechatXml
from wechatimgdb import Wechat_Database
from requestprocessor import RequestProcessor

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome from Mu, this is WeChatImg 0.2'


@app.route('/health')
def api_health():
    return 'Version: 0.2\n' + 'System is up.\n'


@app.route('/messages', methods=['POST', 'GET'])
def api_message():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("program started!")
    token = ConstantValues.token
    if request.method == 'GET':
        response = message_get(request, token)
        return response
    elif request.method == 'POST':
        logging.info("in POST section with Content-Type:" + request.headers['Content-Type'])
        logging.warning("in POST section with data:" + request.data)
        if request.headers['Content-Type'] == 'text/plain':
            return "Text Message: " + request.data
        elif request.headers['Content-Type'] == 'application/json':
            return "JSON Message: " + json.dumps(request.json)
        elif request.headers['Content-Type'] == 'application/xml':
            response = process_xml_posted(request.data)
            return response
        elif request.headers['Content-Type'] == 'text/xml':  # main point of entry for wechat
            logging.info("receive data from " + request.headers["host"])
            response = process_xml_posted(request.data)
            return response
        elif request.headers['Content-Type'] == 'application/octet-stream':
            f = open('./binary', 'wb')
            f.write(request.data)
            f.close()
            return "Binary message written!"
        else:
            logging.warning("in POST section with not handled Content-Type:" + request.headers['Content-Type'])
            return "415 Unsupported Content-Type"

    else:
        return "415 request Type ;)"


def message_get(request, token):
    logger = logging.getLogger(__name__)
    logger.info('Received GET on  /messages of:' + request.query_string)
    signature = request.args.get('signature', '')
    echo_str = request.args.get('echostr', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    logger.debug(echo_str)
    getdata = {'signature': signature, 'echostr': echo_str, 'timestamp': timestamp, 'nonce': nonce}
    this_list = [token, timestamp, nonce, ]
    this_list.sort
    sha1 = hashlib.sha1()
    map(sha1.update, this_list)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return make_response(echo_str)
    else:
        logger.info('hashcode is ' + hashcode + "ERROR, hash doesn't match")
        return make_response(echo_str)


def store_msg_to_db(text_msg_dict, xml):
    """
    :rtype : object
    :param text_msg_dict: dictionary contains parsed info
    :param xml: posted XML from WeChat server
    :return:
    """
    # step 1: connect to db
    logging.info("writing msg details to db")
    if service_prop.DatabaseProperty.isLocalDBHost:
        host = service_prop.DatabaseProperty.local_host
        user = service_prop.DatabaseProperty.local_user
        pwd = service_prop.DatabaseProperty.local_pwd
        db_name = service_prop.DatabaseProperty.local_db_name
        timeout = service_prop.DatabaseProperty.local_timeout
    else:
        host = service_prop.DatabaseProperty.remote_host
        user = service_prop.DatabaseProperty.remote_user
        pwd = service_prop.DatabaseProperty.remote_pwd
        db_name = service_prop.DatabaseProperty.remote_db_name
        timeout = service_prop.DatabaseProperty.remote_timeout
    encoding = service_prop.DatabaseProperty.encoding
    table_name = 'msg'

    try:
        con = mdb.connect(host=host, user=user, passwd=pwd, db=db_name, connect_timeout=timeout, charset=encoding)
        cur = con.cursor()

        #  step 2: construct insert mysql script
        mysql_insert_script_base = "INSERT INTO %s VALUES ('%s','%s','%s','%s','%s', NOW());"
        mysql_script = mysql_insert_script_base % (
            table_name, text_msg_dict['message_id'], text_msg_dict['content'], text_msg_dict['fromuser_id'], xml,
            'comments')
        logging.info("mysql script to run is " + mysql_script)

        #  step 3: execute insert
        try:
            cur.execute(mysql_script)
            con.commit()
        except:
            con.rollback()
            logging.error("error in executing sql script" + mysql_script)
    except mdb.Error as e:
        print("something is not right")

    finally:
        if con:
            con.close()
            logging.info("Closing out db connection")


def construct_response_msg(msg_info, wechatdata):
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName>" \
            "<![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]>" \
            "</Content></xml>"
    if wechatdata.is_image:
        response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
                                service_prop.ConstantValues.ReturnTextStr_PhotoSaved)
    elif wechatdata.is_video:
        response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
                                u'视频已经为您保存')
    elif wechatdata.is_request:
        response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
                                msg_info['content'])
    else:
        response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
                                 service_prop.ConstantValues.ReturnTextStr_PleaseSendPhotoToSave)
    response = make_response(response_xml)
    response.content_type = 'application/xml'
    logging.info("responded with xml: " + response_xml)
    return response

def is_request_image_back(content_dict):
    if service_prop.DownloadPhotosProperty.request_str == content_dict['content']:
        return True
    else:
        return False
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
    # form response
    response = construct_response_msg(msg_info, wechatdata)
    return response


if __name__ == '__main__':
    app.run()
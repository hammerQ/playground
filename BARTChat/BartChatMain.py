# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'
import hashlib
import logging
import urllib.request

from flasgger import Swagger
from flask import Flask, request, json, make_response

from Tools.wechatXMLProcessor import WechatXMLProcessor
from .BARTXMLprocessor import BARTXMLProcessor
from .BartchatProperties import BARTAPI

app = Flask(__name__)
Swagger(app)

@app.route('/')
def api_root():
    return 'Welcome from Mu, this is BARTChat 0.1 with microservices'


@app.route('/health')
def api_health():
    return 'Version: 0.1.0\n' + 'System is up.\n'


@app.route('/messages', methods=['POST', 'GET'])
def api_message():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("program started!")
    token = 'iBuildGoodApp4Ppl'
    if request.method == 'GET':  # this is the authentication step
        response = message_get(request, token)
        return response
    elif request.method == 'POST':
        logging.info("in POST section with Content-Type:" + request.headers['Content-Type'])
        logging.warning("in POST section with data:" + request.data)

        if request.headers['Content-Type'] == 'text/xml':  # main point of entry for wechat
            logging.info("receive data from " + request.headers["host"])
            logging.info("Input XML: " + request.data)
            user_request = process_incoming_wechatXML(request.data)
            BART_response_based_on_usr_request = make_request_2_BART_currentstation(user_request)
            response = construct_response(user_request, BART_response_based_on_usr_request)
            return response
        elif request.headers['Content-Type'] == 'text/plain':
            return "Text Message: " + request.data
        elif request.headers['Content-Type'] == 'application/json':
            return "JSON Message: " + json.dumps(request.json)
        elif request.headers['Content-Type'] == 'application/xml':
            response = "something "  # process_xml_posted(request.data)
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


def process_incoming_wechatXML(xml):
    """Process the incoming wechatXML specifically for BART chat
    :param xml: incoming xml from WeChat server that contains user info ans user request
    :return: dictionary of the incoming wechat xml
    """
    return WechatXMLProcessor.process_xml_posted(xml)

def make_request_2_BART_currentstation(user_request):
    """
    make request to BART API
    :param user_request: 
    :return: xml structure from BART
    """
    if user_request:
        current_station_str = user_request['content']
        #TODO: use current station input from user
        BART_response_xml = urllib.request.urlopen(BARTAPI.BART_EXAMPLE_REQUEST).read()
        logging.info('BART Response XML is:' + BART_response_xml)
        return BART_response_xml
    else:
        return None

def construct_response(msg_info, BART_response_xml):
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName>" \
            "<![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]>" \
            "</Content></xml>"
    BART_API_response_Dict = BARTXMLProcessor.process_xml_posted(BART_response_xml)
    # if wechatdata.is_image:
    #     response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
    #                             service_prop.ConstantValues.ReturnTextStr_PhotoSaved)
    # elif wechatdata.is_video:
    #     response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
    #                             u'视频已经为您保存')
    # elif wechatdata.is_request:
    #     response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
    #                             msg_info['content'])
    # else:
    #     response_xml = reply % (msg_info['fromuser_id'], msg_info['wechatimg_id'], str(int(time.time())),
    #                             service_prop.ConstantValues.ReturnTextStr_PleaseSendPhotoToSave)
    # response = make_response(response_xml)
    # response.content_type = 'application/xml'
    # logging.info("responded with xml: " + response_xml)
    response = 'response something'
    return response

def determine_if_BART_has_error(BART_response_xml):
    """
    Determine is BART is responsing temporarily unavailable
    :param BART_response_xml: 
    :return: True if BART is temporarily unavailable
    """
    BARTXMLProcessor()



if __name__ == '__main__':
    app.run()
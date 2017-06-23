# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'
import logging
from flask import Flask, request, json, make_response
from flasgger import Swagger
import untangle
import hashlib

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
            JSON_obj = convert_xml_to_JSON(request.data)
            logging.info("Input XML converted to JSON: " + JSON_obj)
            response = construct_response()
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

def convert_xml_to_JSON(xml):
    """
    convert incoming xml to JSON object for internal consumption
    :param xml: 
    :return: JSON response
    """
    obj = untangle.parse(xml)
    return obj

def construct_response(msg_info, wechatdata):
    # reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName>" \
    #         "<![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime>" \
    #         "<MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]>" \
    #         "</Content></xml>"
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

if __name__ == '__main__':
    app.run()
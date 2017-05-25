__author__ = 'mqiao'
import logging
from flask import Flask, url_for, request, json, Response, make_response
import hashlib

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome from Mu'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/health')
def api_health():
    return 'Version: 0.1\n' + 'System is up.\n'

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name'] + '\n'
    else:
        return 'Hello John Doe\n'
@app.route('/echo', methods=['GET'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

@app.route('/messages', methods=['POST','GET'])
def api_message():
    logger = logging.getLogger(__name__)
    token = 'iBuildGoodApp4Ppl'
    if request.method == 'GET':
        response = messageget(request,token)
        return response
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            return "Text Message: " + request.data
        elif request.headers['Content-Type'] == 'application/json':
            return "JSON Message: " + json.dumps(request.json)
        elif request.headers['Content-Type'] == 'applicaiton/xml':
            logging.info('getting XML message' + request.data)
            return "XML Message: " + request.data


        elif request.headers['Content-Type'] == 'application/octet-stream':
            f = open('./binary', 'wb')
            f.write(request.data)
            f.close()
            return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"


def messageget(request,token):
    logger = logging.getLogger(__name__)
    logger.info('Received GET on  /messages of:' + request.query_string)
    signature = request.args.get('signature','')
    echostr = request.args.get('echostr','')
    timestamp = request.args.get('timestamp','')
    nonce = request.args.get('nonce','')
    logger.debug(echostr)
    getdata = {'signature': signature, 'echostr': echostr, 'timestamp': timestamp, 'nonce': nonce}
    s = [timestamp, nonce, token]
    s.sort
    s = ''.join(s)
    if ( hashlib.sha1(s).hexdigest() == signature ):    
        return make_response(echostr) 
    else:
        return make_response(echostr)

if __name__ == '__main__':
    app.run()
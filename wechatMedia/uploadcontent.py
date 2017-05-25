# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'
import logging
import properties as service_prop
import requests



class UploadContent():
    basePostURL = None
    mediaType = None
    accessToken = None


    def __init__(self, mediaTypeStr, accessTokenStr):
        self.mediaType = mediaTypeStr
        self.accessToken = accessTokenStr
        self.basePostURL = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (self.accessToken,
                                                                                                       self.mediaType)

    def uploadData2WeChatServer(self, data):
        myRequest = requests.post(self.basePostURL, data=data)
        logging("respons is " + myRequest.json())

        # params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
        # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        # conn = httplib.HTTPConnection("bugs.python.org")
        # conn.request("POST", "", params, headers)
        # response = conn.getresponse()
        # print response.status, response.reason

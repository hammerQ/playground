# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import logging
import properties as service_prop
import urllib2
from datetime import datetime
import hashlib

class WechatStorage():
    is_local_storage = True
    input_url = None
    stored_url = None
    is_image = None
    is_video = None

    def __init__(self, inputval):
        self.input_url = inputval
        self.is_local_storage = service_prop.StorageProperty.isLocalStorage
        self.storage_domain_name = service_prop.StorageProperty.remote_storage_domain_name


    def store_image(self):

        """
        download image from WeChat url and store in storage. update stored_url
        """
        try:
            response = urllib2.urlopen(self.input_url)

            if self.is_local_storage:
                # just use the current url
                self.stored_url = self.input_url

            else:
                # save to remote storage
                from sae.storage import Bucket
                # print ("in else "+self.storage_domain_name)
                bucket = Bucket('wechatimgsave')
                filename = self.definefilename(self.input_url, '.jpeg')
                bucket.put_object(obj=filename, contents=response.read(), content_type='image/jpeg',
                                  content_encoding=None, metadata=None)
                self.stored_url = bucket.generate_url(filename)

        except urllib2.HTTPError as e:
            logging.error("Error in opening " + self.input_url + "with error code: "+e.code)

    def set_islocalstorage(self, value):
        self.is_local_storage = value

    def definefilename(self, input_url, extension):
        m = hashlib.md5()
        m.update(input_url)
        return datetime.now().strftime("%Y%m%d%H%M%S")+'_'+m.hexdigest()+extension






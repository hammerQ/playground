# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import properties as service_prop

class RequestProcessor():

    def __init__(self, dict):
        self.dict = dict

    def uploadAllPhotosOfUser(self):
        # 1. based on user id query certain # image url from mysql (earliest first)
        # 2. upload each one of photos as temporary media (earliest first), record corresponding media id
        # 3. send photos (via media id) to user

        numberofPhotos = service_prop.DownloadPhotosProperty.numberofPhotos

        return 'downloading photos for you!'+' Userid: ' + self.dict['fromuser_id']

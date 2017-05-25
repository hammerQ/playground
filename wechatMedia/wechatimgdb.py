# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'
import logging
import properties as service_prop

import datetime
import MySQLdb as mdb
import requests
from wechatimgstorage import WechatStorage


class Wechat_Database():

    info_dict = dict()
    is_local_db_host = True
    is_local_storage = True

    def __init__(self,  wechatdata):
        self.info_dict = wechatdata.xlm_content_dict
        self.is_local_db_host = service_prop.DatabaseProperty.isLocalDBHost
        self.is_local_storage = service_prop.StorageProperty.isLocalStorage
        self.determine_db_properties()
        self.encoding = service_prop.DatabaseProperty.encoding
        self.image_table_name = service_prop.DatabaseProperty.image_table_name
        self.accesstoken_table_name = service_prop.DatabaseProperty.accesstoken_table_name
        self.wechatdata = wechatdata

    def construct_mysql_script_4_insert_img_table(self, image_table_name, xml):
        mysql_insert_script_base = "INSERT INTO %s VALUES ('%s','%s','%s','%s','%s',NULL,'%s',NOW());"
        create_time = datetime.datetime.fromtimestamp(float(self.info_dict['create_time']))
        # print "time is " + create_time.strftime('%Y-%m-%d %H:%M:%S')
        self.mysql_script = mysql_insert_script_base % (
            image_table_name, self.info_dict['media_id'], self.info_dict['picture_url'],
            self.info_dict['fromuser_id'], xml, 'comments', create_time.strftime('%Y-%m-%d %H:%M:%S'))
        logging.info("mysql script to run is " + self.mysql_script)

    def determine_db_properties(self):
        if self.is_local_db_host:
            self.db_host_master = service_prop.DatabaseProperty.local_host
            self.user = service_prop.DatabaseProperty.local_user
            self.pwd = service_prop.DatabaseProperty.local_pwd
            self.db_name = service_prop.DatabaseProperty.local_db_name
            self.timeout = service_prop.DatabaseProperty.local_timeout
            self.port = service_prop.DatabaseProperty.local_port
        else:
            self.db_host_master = service_prop.DatabaseProperty.remote_host
            self.user = service_prop.DatabaseProperty.remote_user
            self.pwd = service_prop.DatabaseProperty.remote_pwd
            self.db_name = service_prop.DatabaseProperty.remote_db_name
            self.timeout = service_prop.DatabaseProperty.remote_timeout
            self.port = service_prop.DatabaseProperty.remote_db_port
            self.db_host_slave = service_prop.DatabaseProperty.remote_host_s

    def obtain_url_4_storage(self):
        if self.wechatdata.is_image:
            final_url = self.get_stored_image_url(self.info_dict['picture_url'])
        elif self.wechatdata.is_video:
            final_url = self.get_stored_video(self.info_dict['media_id'])
        return final_url

    def store_media_info_to_db(self, xml):
        """
        writing image msg details to db image table
        :param xml: posted xml from WeChat server
        """
        # step 1: determine db properties
        self.determine_db_properties()
        # step 2: save to SAE storage if remote host
        final_url = self.obtain_url_4_storage()
        logging.info("storage url is "+final_url)
        self.info_dict['picture_url'] = final_url

        # step 3: connect to db and insert info.

        try:
            con = mdb.connect(host=self.db_host_master, user=self.user, passwd=self.pwd, db=self.db_name,
                              connect_timeout=self.timeout, port=self.port, charset=self.encoding)
            cur = con.cursor()
            self.construct_mysql_script_4_insert_img_table(self.image_table_name, xml)
            #  step 4: execute insert
            try:
                cur.execute(self.mysql_script)
                con.commit()
            except:
                con.rollback()
                logging.error("error in executing sql script" + self.mysql_script)
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:
            if con:
                con.close()
                logging.info("Closing out db connection")

    def get_stored_image_url(self, url):
        storage = WechatStorage(url)
        storage.is_image = True
        storage.store_image()
        return storage.stored_url

    def set_islocaldbhost(self, value):
        self.is_local_db_host = value

    def set_islocalstorage(self, value):
        self.is_local_storage = value

    def get_stored_video(self, mediaID):
        storage = WechatStorage(mediaID)
        storage.is_video = True
        #   http://mp.weixin.qq.com/wiki/11/07b6b76a6b6e8848e855a435d5e34a5f.html
        #   use media id and access url to download video
        storage.store_image()
        return storage.stored_url

    def read_access_token_fromDB(self):
        """ This method use UTC time. read access token from db table accesstoken.
        :return: dict([('accesstoken', accesstoken), ('tokenstart',tokenstart)])
        """
        #   step 1 reads db to get token and tokenstart
        self.determine_db_properties()
        try:
            dbconnection = mdb.connect(host=self.db_host_master, user=self.user, passwd=self.pwd, db=self.db_name,
                              connect_timeout=self.timeout, port=self.port, charset=self.encoding)
            cursor = dbconnection.cursor()
            readscript_accesstoken = self.construct_read_accesstoken_fromdb(self.accesstoken_table_name)
            #  step 4: execute read
            try:
                cursor.execute(readscript_accesstoken)
                results = cursor.fetchone()
                stored_token = results[0]
                stored_token_start_time = results[1]
            except:
                logging.error("error in executing sql script" + readscript_accesstoken)
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:
            if dbconnection:
                dbconnection.close()
                logging.info("Closing out db connection")

        return dict([('accesstoken', stored_token), ('tokenstart', stored_token_start_time)])

    def get_valid_access_token(self):
        """ This method use UTC time. read access token from db table accesstoken. If token hasn't expired, it
        returns access token. Fetch a new access token from Tencent if expired.
        """
        current_token_dict = self.read_access_token_fromDB()
        token = current_token_dict['accesstoken']
        token_start_timeUTC= current_token_dict['tokenstart']
        currentUTC = datetime.datetime.utcnow()
        time_diff_sec = (currentUTC - token_start_timeUTC).seconds
        if time_diff_sec < (service_prop.WeChatSysProperty.AccessTokenValidationTime_Sec - service_prop.WeChatSysProperty.AccessTokenValidationBufferTime_Sec):
            return token
        else:   # need to get new token and store this token in db.
            new_token_dict = self.get_new_token_from_tencent()
            self.store_new_token_and_time_inDB(new_token_dict);
            return new_token_dict['accesstoken']


    def get_new_token_from_tencent(self):
        result_from_tencent = (requests.get(service_prop.WeChatSysProperty.geturl_4_access_token()).json())
        logging.info("new access token is " + result_from_tencent['access_token'])
        if result_from_tencent['expires_in'] != 7200:
            logging.error("Expiration time changed")
        return dict([('accesstoken', result_from_tencent['access_token']), ('tokenstart', datetime.datetime.utcnow())])

    #TODO:
    def store_new_token_and_time_inDB(self, access_token_dict):
        return ""
    def construct_read_accesstoken_fromdb(self, table_name):
        """ This method construct read script to get access token and token start datetime from db
        :return:
        """
        mysql_read_script_base = "SELECT * from %s ;"
        mysql_script = mysql_read_script_base % (table_name)
        logging.info("mysql script to run is " + mysql_script)
        return mysql_script

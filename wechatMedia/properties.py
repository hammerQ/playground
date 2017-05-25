# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'


class DatabaseProperty:
    """Contains property values related to database
    """
    isLocalDBHost = True  # This needs to be False for SAE
    timeout = 10  # second
    image_table_name = 'image'
    accesstoken_table_name = 'accesstoken'

    encoding = 'utf8'  # WeChatImg db's varchar is utf8
    local_host = 'localhost'
    local_user = 'hammer'
    local_pwd = 'helpu$'
    local_db_name = 'wechatdb'
    local_timeout = timeout
    local_port = 3307

    if not isLocalDBHost:
        import sae.const
        remote_host = sae.const.MYSQL_HOST    # 主库域名（可读写）
        remote_host_s = sae.const.MYSQL_HOST_S  # 从库域名（只读）
        remote_user = sae.const.MYSQL_USER    # 用户名
        remote_pwd = sae.const.MYSQL_PASS    # 密码
        remote_db_name = sae.const.MYSQL_DB      # 数据库名
        remote_db_port = int(sae.const.MYSQL_PORT)	# 端口，类型为<type 'str'>，请根据框架要求自行转换为int
        remote_timeout = timeout

class ConstantValues:
    """Contain constant values used by service

    """
    ReturnTextStr_PleaseSendPhotoToSave = u'请上传图片，我们为您保存'
    ReturnTextStr_PhotoSaved = u'图片已经为您保存'
    token = 'iBuildGoodApp4Ppl'

class StorageProperty:
    """ Contains property values related to storage

    """
    isLocalStorage = True   # This needs to be False for SAE
    remote_storage_domain_name = 'wechatimgsave'

class DownloadPhotosProperty:
    """ Contains property values related to download photos

    """
    request_str = 'my photos'
    numberofPhotos = 10

class WeChatSysProperty:
    """ Contains property values related to WeChat/Tencent backend system

    """
    AccessTokenValidationTime_Sec = 7200    # seconds
    AccessTokenValidationBufferTime_Sec = 5     # giving some buffer time for expiration
    AccessTokenValidationTime_mSec = AccessTokenValidationTime_Sec*1000     # in millisecond
    BaseURL4AccessToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    AppID = "wx0e8510887f4eff17"
    AppSecret = "1e7b2f1ede267654bc8cdcd2cdef3a70"

    def geturl_4_access_token(self):
        return self.BaseURL4AccessToken % (self.AppID, self.AppSecret)
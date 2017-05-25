# This Python file uses the following encoding: utf-8
# encoding: utf-8
__author__ = 'mqiao'

import MySQLdb as mdb
import sys
import properties
try:
    if properties.DatabaseProperty.isLocalDBHost:
        host = properties.DatabaseProperty.local_host
        user = properties.DatabaseProperty.local_user
        pwd = properties.DatabaseProperty.local_pwd
        db_name = properties.DatabaseProperty.local_db_name
        timeout = properties.DatabaseProperty.local_timeout
    else:
        host = properties.DatabaseProperty.remote_host
        user = properties.DatabaseProperty.remote_user
        pwd = properties.DatabaseProperty.remote_pwd
        db_name = properties.DatabaseProperty.remote_db_name
        timeout = properties.DatabaseProperty.remote_timeout

    encoding = properties.DatabaseProperty.encoding

    con = mdb.connect(host=host, user=user, passwd=pwd, db=db_name, connect_timeout=timeout, charset=encoding)
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print "Database version : %s " % ver
    cur.execute("select * from msg;")
    print cur.fetchall()[1][4]
    try:
        cur.execute("INSERT INTO msg VALUES ('6172892165281362744','Abc','oMwf3s4hyHHp1eKxyyiCpb8is9oQ',"
                       "'<xml><ToUserName><![CDATA[gh_bf693268132e]]></ToUserName><FromUserName>"
                       "<![CDATA[oMwf3s4hyHHp1eKxyyiCpb8is9oQ]]></FromUserName><CreateTime>1437238456</CreateTime>"
                       "<MsgType><![CDATA[text]]></MsgType><Content><![CDATA[123456789]]></Content>"
                       "<MsgId>6172892165281362744</MsgId></xml>', '第2个信息', NOW());")
        con.commit()
    except:
        con.rollback()

    # ver = cur.fetchall()
    # print ver

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()

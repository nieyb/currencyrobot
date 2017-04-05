#coding=utf8
import thread

import itchat
import time, sys
from itchat.content import *

replyToGroupChat = True
functionStatus = False

reload(sys)
sys.setdefaultencoding('utf8')

newInstance = itchat.new_instance()

@newInstance.msg_register(TEXT)
def reply(msg):
    return msg['Text']


# 朋友text 聊天处理
@newInstance.msg_register(TEXT)
def text_reply_text(msg):
    print "===============朋友text 聊天处理======newInstance====text_reply_text========================="
    print msg


if __name__ == '__main__':
    if "linux" in sys.platform:
        enable_cmd_qr = 2
    else:
        enable_cmd_qr = False

    # newInstance.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, statusStorageDir='newInstance.pkl')
    newInstance.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, statusStorageDir='newInstance.pkl')
    newInstance.run(debug=True, blockThread=True)


    # itchat.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, picDir=False, qrCallback=None, loginCallback=None,
    #                   exitCallback=None)
    # itchat.run(debug=True, blockThread=True)

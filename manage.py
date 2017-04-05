# -*- coding: utf-8 -*-
from robot.index import run_index

if __name__ == '__main__':
    run_index()

#
# import sys, itchat
# from itchat.content import *
#
# reload(sys)
# sys.setdefaultencoding('utf8')
#
#
# if __name__ == '__main__':
#     if "linux" in sys.platform:
#         enable_cmd_qr = 2
#     else:
#         enable_cmd_qr = False
#     itchat.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, picDir=False, qrCallback=None, loginCallback=None,
#                       exitCallback=None)
#     itchat.run(debug=True, blockThread=True)

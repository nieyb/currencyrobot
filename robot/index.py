# -*- coding:utf-8 -*-
"""
机器人启动index
"""
import datetime
import json
import sys
import time

import itchat
from config import oss_url_2, oss_url_1, sms_msg_1, add_friend_msg
from itchat.content import *
from robot.service import service_handle
from robot.util.redis_conf import predis
from robot.util.oss import upload_file_images_to_oss, itchat_upload_images_to_oss, get_random_name
from tuling_jiqiren.tuling_1 import robot_reply
from robot import constants


reload(sys)
sys.setdefaultencoding('utf8')

new_instance_b = itchat.new_instance()






def get_login_robot():
    myself_info = new_instance_b.get_friends(update=True)[0]
    return myself_info["NickName"], myself_info["Uin"]


@new_instance_b.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print "66666666666666666666666", msg['Type']
    print msg
    new_instance_b.send('%s' % (msg['Text']), msg['FromUserName'])


@new_instance_b.msg_register([SHARING], isGroupChat=True)
def text_reply(msg):
    print "===============分享======================="
    print msg
    msg["jiqiren_name"], msg["jiqiren_uin"] = get_login_robot()
    service_handle.q_into_text(new_instance_b, msg)
    # new_instance_b.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@new_instance_b.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print "===========download_files==========="
    print msg

    jqr = dict()
    jqr["jqr_name"], jqr["jqr_uin"] = get_login_robot()

    code = "look_msg"
    from_user_name = msg['FromUserName']
    to_user_name = msg['ToUserName']
    msg_type = msg['Type'] #文件类型

    """上传文件存储到阿里云"""
    x = msg['Text']()
    #file_name = msg["FileName"]

    file_type = (msg["FileName"]).split('.')[1]
    file_name = get_random_name(file_type)

    url_name = oss_url_2 + file_name
    url_name_1 = oss_url_1 + file_name
    x = upload_file_images_to_oss(x, url_name)
    print url_name_1

    """查找发文件人信息"""
    search_friend = service_handle.search_friends(new_instance_b, userName=from_user_name)

    """存储好友聊天信息"""
    friend_data = service_handle.friend_into_text2(jqr=jqr, content=url_name_1, to_user_name=to_user_name,
                                                   search_friend=search_friend, msg_type=msg_type)

    """从缓存不断获取发送消息， 指导输入结束，结束本次文字加图片的发送"""
    redis_content = predis.get(name=msg['FromUserName'])
    if redis_content:
        """多条消息连在一起"""
        redis_content = json.loads(redis_content)
        redis_content[1] += "{{"+url_name_1+"}}"
        redis_content = json.dumps(redis_content)
        predis.set(name=msg['FromUserName'], value=redis_content)
        new_instance_b.send("收到,完成后发送'结束'.", msg['FromUserName'])
    else:
        """发送单条消息"""
        service_handle.friend_into_text2(jqr=jqr, content=url_name_1, to_user_name=to_user_name, search_friend=search_friend,
                                         msg_type=msg_type)
        if "KeyWord" in search_friend:
            KeyWord = search_friend["KeyWord"]
        else:
            KeyWord = ""
        Alias = search_friend["Alias"] if search_friend["Alias"] else "not_Alias_to_key_word"
        user_list = service_handle.sql_search_user(Alias=Alias, keyword=KeyWord)
        if not user_list:
            user_list = service_handle.sql_search_user(userName=msg['FromUserName'])
        print "##user_list##", user_list
        notice_info_list = service_handle.into_edu_school_notice(content="{{" + url_name_1 + "}}", to_user_name=to_user_name,
                                                                 user_list=user_list, content_class_name="")
        print "###notice_info_list###", notice_info_list
        for notice_info in notice_info_list:
            print notice_info
            """生成短链接"""
            msg_url = service_handle.handel_send_url(notice_info, code)
            if code == "class_msg":
                msg_url = notice_info["school_class_name"] + msg_url
                new_instance_b.send(msg_url, msg['FromUserName'])
            else:
                if notice_info["school_class_user_name"]:
                    msg_url = sms_msg_1.format(notice_info["user_displayname"],str(datetime.datetime.now())[:16]) + msg_url
                    new_instance_b.send(msg_url, notice_info["school_class_user_name"])
                else:
                    new_instance_b.send(u"获取班级信息错误，请在微信群里@机器人。", msg['FromUserName'])


    # new_instance_b.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
    # return '%s received' % msg['Type']
    # msg['Text'](msg['FileName'])
    # #print '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@new_instance_b.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files(msg):
    print "======群图片信息=========="
    msg["jiqiren_name"], msg["jiqiren_uin"] = get_login_robot()
    import config
    if config.OPEN_ROOM_FILE:
        if msg["Type"] == 'Picture':
            img_io = msg['Text']()
            # show_url = itchat_upload_images_to_oss(img_io)

            file_type = (msg["FileName"]).split('.')[1]
            file_name = get_random_name(file_type)

            url_name = oss_url_2 + file_name
            show_url = oss_url_1 + file_name
            x = upload_file_images_to_oss(img_io, url_name)

            print show_url
            msg['Content'] = show_url
        """存储群聊天信息"""
        print "=================存储群聊天信息========================="
        service_handle.q_into_text(new_instance_b, msg)


# 朋友text 聊天处理
@new_instance_b.msg_register(TEXT)
def text_reply_text(msg):
    print "===============朋友text 聊天处理=====text_reply_text================="
    content = msg["Content"].lstrip(' ')
    print "##content##", content
    from_user_name = msg['FromUserName']
    to_user_name = msg['ToUserName']
    code = "look_msg"
    content_class_name = ""
    content_cmd = content
    msg_type = "text"

    jqr = dict()
    jqr["jqr_name"], jqr["jqr_uin"] = get_login_robot()

    print "==============name, uin=================="
    if content.strip() == constants.UPDATE_FRIENDS_KEY:
        """手动输入同步好友信息"""
        print "===========itchat===开始同步好友信息========================="
        friends = new_instance_b.get_friends(update=True)[1:]
        begin_time_now = datetime.datetime.now()
        service_handle.sync_friends(new_instance_b, friends, jqr)
        end_time_now = datetime.datetime.now()
        last_time = end_time_now - begin_time_now
        print "===同步好友信息完成,开始时间:", begin_time_now
        print "===结束时间:", end_time_now
        print "===总共花费时间：", last_time

    if content.strip() == constants.UPDATE_ROOMS_KEY:
        """手动输入同步群信息"""
        print "===========itchat===开始同步群信息========================="
        rooms = new_instance_b.get_chatrooms(update=True)
        begin_time_now = datetime.datetime.now()
        service_handle.sync_rooms(new_instance_b, rooms, jqr)
        end_time_now = datetime.datetime.now()
        last_time = end_time_now - begin_time_now
        print "===同步群信息完成,开始时间:", begin_time_now
        print "===结束时间:", end_time_now
        print "===总共花费时间：", last_time

    search_friend = service_handle.search_friends(new_instance_b, userName=from_user_name)

    redis_content = predis.get(name=msg['FromUserName'])

    if redis_content and content_cmd != constants.END_MESSAGES:
        redis_content = json.loads(redis_content)
        redis_content[1] += "{{"+content_cmd+"}}"
        redis_content = json.dumps(redis_content)
        predis.set(name=msg['FromUserName'], value=redis_content)
        return new_instance_b.send("收到,完成后发送'结束'.", msg['FromUserName'])


    if content.strip() == constants.HELP:
        """输入使用说明， 返回帮助链接 """
        help_url = service_handle.xin_lang_convert_short_url(constants.HELP_URL)
        return new_instance_b.send('%s: %s' % ("点滴机器人使用说明", help_url), msg['FromUserName'])

    flag = False
    if constants.AT_SEND_MESSAGES in content or constants.AT_MANAGE_CLASS_KEY in content:
        """判断是否给单个群发信息, @发消息， @班级管理"""
        content_list = content.split("@")
        if len(content_list) == 2:
            content_class_name = content_list[0]
            content_cmd = content_list[1]
            flag = True
            print "=============@发消息=============", content_cmd
    elif not content_cmd in constants.CMD_DATA_LIST and not content_cmd.startswith(constants.SEND_MESSAGES) \
            and content_cmd != constants.SEND_MESSAGES:
        """跟机器人聊天返回信息"""
        jiqiren_msg = robot_reply(content_cmd, uid=msg['FromUserName'])

        """存聊天信息"""
        friend_data = service_handle.friend_into_text2(jqr=jqr, content=content_cmd, to_user_name=to_user_name,
                                                       search_friend=search_friend, msg_type=msg_type)

        return new_instance_b.send(jiqiren_msg, msg['FromUserName'])

    if content_cmd == constants.MANAGE_CLASS_KEY:
        """班级管理"""
        code = "class_msg"

    if content_cmd == constants.SEND_MESSAGES:
        """开始输入发送多条消息"""
        predis.set(name=msg['FromUserName'], value=json.dumps([content_class_name, ""]))
        return new_instance_b.send("请输入文字内容:", msg['FromUserName'])

    if content_cmd == constants.END_MESSAGES:
        """输入结束， 完成一次发送多条消息"""
        if redis_content:
            redis_content = json.loads(redis_content)
            content_class_name = redis_content[0]
            content_cmd = redis_content[1]
            predis.delete(msg['FromUserName'])
            new_instance_b.send("完成。", msg['FromUserName'])

    if content.startswith(constants.SEND_MESSAGES) and content != constants.SEND_MESSAGES:
        content_cmd = content.lstrip(constants.SEND_MESSAGES).lstrip('：').lstrip(':').strip()
        content_cmd = "{{"+content_cmd+"}}"

    friend_data = service_handle.friend_into_text2(jqr=jqr, content=content_cmd, to_user_name=to_user_name,
                                                   search_friend=search_friend, msg_type=msg_type)

    print "=================search_friend=================", search_friend
    if "KeyWord" in search_friend:
        KeyWord = search_friend["KeyWord"]
    else:
        KeyWord = ""

    Alias = search_friend["Alias"] if search_friend["Alias"] else "not_Alias_to_key_word"
    user_list = service_handle.sql_search_user(Alias=Alias, keyword=KeyWord)

    if not user_list:
        user_list = service_handle.sql_search_user(userName=msg['FromUserName'])

    print "=================user_list==================="
    print user_list

    """如果flag为true, 则单个群发消息"""
    if flag:
        print "==================flag===========", flag
        content_cmd = content_cmd.lstrip(constants.SEND_MESSAGES).lstrip('：').lstrip(':').strip()
        content_cmd = "{{"+content_cmd+"}}"

    """存入消息表"""
    notice_info_list = service_handle.into_edu_school_notice(content=content_cmd, to_user_name=to_user_name,
                                                             user_list=user_list, content_class_name=content_class_name)
    for notice_info in notice_info_list:
        """把消息处理成短链接发送"""
        msg_url = service_handle.handel_send_url(notice_info, code)
        print "=================发送短链接拉====================="
        if code == "class_msg":
            print "===================class-msg===================="
            msg_url = notice_info["school_class_name"] + msg_url
            """回复老师的问题"""
            new_instance_b.send(msg_url, msg['FromUserName'])
        else:
            if notice_info["school_class_user_name"] and not flag:
                print "==========66666666666666666666666666"
                msg_url = sms_msg_1.format(notice_info["user_displayname"], str(datetime.datetime.now())[:16]) + msg_url
                new_instance_b.send(msg_url, notice_info["school_class_user_name"])
            elif notice_info["school_class_name"] == content_class_name and flag:
                msg_url = sms_msg_1.format(notice_info["user_displayname"], str(datetime.datetime.now())[:16]) + msg_url
                new_instance_b.send(msg_url, notice_info["school_class_user_name"])
            else:
                print "============77777777777777777========================="
                new_instance_b.send(u"获取班级信息错误，请在微信群里@机器人。", msg['FromUserName'])


# 收到好友邀请自动添加好友
@new_instance_b.msg_register(FRIENDS)
def add_friend(msg):
    print "##add_friend##", msg
    new_instance_b.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    new_instance_b.send(add_friend_msg, msg['RecommendInfo']['UserName'])


# 群 text消息处理
@new_instance_b.msg_register(TEXT, isGroupChat=True)
def groupchat_reply(msg):
    print "=======================群 text消息处理 groupchat_reply===================="
    """
    在注册时增加isGroupChat=True将判定为群聊回复
    [PICTURE, RECORDING, ATTACHMENT, VIDEO]
    isAt: 判断是否@本号,ActualNickName: 实际NickName,Content: 实际Content
    """
    content = msg["Content"].lstrip(' ')
    q_username = msg['FromUserName']
    chat_room = new_instance_b.search_chatrooms(userName=q_username)
    room_uin = chat_room["Uin"]
    room_nick_name = chat_room["NickName"]
    print "====room_uin======room_nick_name==========="
    print room_uin, room_nick_name
    if content.strip() == constants.HELP:
        """输入使用说明， 返回帮助链接 """
        help_url = service_handle.xin_lang_convert_short_url(constants.HELP_URL)
        return new_instance_b.send('%s: %s' % ("点滴机器人使用说明", help_url), msg['FromUserName'])

    if content.strip() == constants.GROW:
        """输入成长日志， 返回成长日志链接 """
        print "========成长日志从这里开始=========="
        if room_uin:
            c_room = service_handle.service_search_room_id_by_uin(room_uin)
        else:
            c_room = service_handle.service_search_room_id_by_nick_name(room_nick_name)

        print "=============成长日志 room=============="
        print c_room
        if c_room:
            room_id = str(c_room.id)
            print "===成长日志 room id==", room_id
            r_url = "http://jx.diandiyun.com/wx/robots/rooms/"+room_id+"/robotlog"
            print "====发送加密前的===成才日志===url==="
            print r_url
            room_url = service_handle.xin_lang_convert_short_url(r_url)
            print "====发送加密后的===成才日志===url==="
            print room_url
            return new_instance_b.send('%s: %s' % ("点击查看成长日志", room_url), msg['FromUserName'])
        error_msg = u'暂无日志查看'
        print "=========================成长日志， 没有日志可看============="
        return new_instance_b.send(error_msg, msg['FromUserName'])

    msg["jiqiren_name"], msg["jiqiren_uin"] = get_login_robot()

    if msg['isAt']:
        print "============begin isAt============================"
        print msg
        print "============end isAt==================================="
        """更新群成员信息"""
        service_handle.q_isat_into(new_instance_b, msg)
    else:
        print "===================begin not isAt====================="
        """存储群聊天信息"""
        service_handle.q_into_text(new_instance_b, msg)


# # 群 text消息处理
# @new_instance_b.msg_register(TEXT, isGroupChat=True)
# def groupchat_reply(msg):
#     from_user_name = msg['FromUserName']
#     memberlist = new_instance_b.update_chatroom(from_user_name, detailedMember=True)
#     print "####memberlist####",memberlist

@new_instance_b.msg_register(SYSTEM)
def get_uin(msg):
    """
    开始登录, 初始化数据, 主要有

    :param msg:
    :return:
    """
    if msg['SystemInfo'] != 'uins':
        return
    else:
        pass

    """登录者本人信息"""
    myself_info = new_instance_b.get_friends(update=True)[0]
    print "======robot_info============"
    my_user = new_instance_b.search_friends(userName=myself_info["UserName"])
    recod_id = service_handle.add_robot_self(my_user["NickName"], my_user["Uin"])
    print my_user["Uin"], recod_id
    print "======robot_info============"

    ins = new_instance_b.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    print('** Uin Updated **')
    for username in msg['Text']:
        member = new_instance_b.utils.search_dict_list(fullContact, 'UserName', username)
        nick_name = member.get('NickName', '')
        uin = member['Uin']
        alias = member['Alias']
        user_name = member['UserName']
        EncryChatRoomId = member["EncryChatRoomId"]
        """更新班级信息， 即群信息"""
        if "@chatroom" in uin:
            xcv = new_instance_b.update_chatroom(userName=EncryChatRoomId)
            service_handle.handel_class_update_sys(uin=uin, nick_name=nick_name, user_name=user_name,
                                                   KeyWord=xcv["KeyWord"])
        elif "gh_" in uin:
            print "公众号", uin
        else:
            """更新好友信息"""
            print "好友", uin, alias, nick_name
            if uin and not alias:
                alias = uin
            service_handle.friend_update_sys(uin=uin, nick_name=nick_name, alias=alias, user_name=user_name)


def init_robot_data():
    service_handle.sync_robot_data.delay()


def run_index(key="default"):
    if "linux" in sys.platform:
        enable_cmd_qr = 2
    else:
        enable_cmd_qr = False

    """初始化机器人数据库表"""

    pkl_name = "pkl/robot_" + str(key) + ".pkl"
    new_instance_b.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, picDir=None, qrCallback=None, loginCallback=None,
                      exitCallback=None,  statusStorageDir=pkl_name)
    new_instance_b.run(debug=True, blockThread=True)


if __name__ == '__main__':
    if "linux" in sys.platform:
        enable_cmd_qr = 2
    else:
        enable_cmd_qr = False
    new_instance_b.auto_login(hotReload=True, enableCmdQR=enable_cmd_qr, picDir=None, qrCallback=None, loginCallback=None,
                      exitCallback=None, statusStorageDir='pkl/robot_default.pkl')
    new_instance_b.run(debug=True, blockThread=True)






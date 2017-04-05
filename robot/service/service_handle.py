# -*- coding:utf-8 -*-
import json

import requests
from celery_config import cry

from config import xinlang_url, msg_url_1, rts
from robot.dao import update_user_role, dao_find, dao_sql, dao_add
import service_index
from robot.util.oss import itchat_upload_images_to_oss


def xin_lang_convert_short_url(surl):
    print "=============xin_lang_convert_short_url==============="
    print surl
    data = {"url_long": surl}
    content = requests.get(url=xinlang_url, params=data)
    xx = json.loads(content.content)
    return xx[0]["url_short"]


def handel_send_url(notice_info, code):
    print "=================handel_send_url=========================="
    print notice_info
    msg_url = msg_url_1
    msg_url += "?class_id_list=" + str(notice_info["school_class_id"])
    msg_url += "&notice_id=" + str(notice_info["notice_id"])
    msg_url += "&user_id=" + str(notice_info["from_id"])
    msg_url += "&mark_msg=" + code
    msg_url = xin_lang_convert_short_url(msg_url)
    return msg_url


def search_friends(new_instance_b, name=None, userName=None, remarkName=None, nickName=None,wechatAccount=None):
    """根据名称查好友信息"""
    search_friends_dict = {}
    search_friends = new_instance_b.search_friends(name=name, userName=userName, remarkName=remarkName, nickName=nickName,wechatAccount=wechatAccount)
    if search_friends:
        search_friends_dict["UserName"] = search_friends["UserName"]
        search_friends_dict["DisplayName"] = search_friends["DisplayName"]
        search_friends_dict["NickName"] = search_friends["NickName"]
        search_friends_dict["HeadImgUrl"] = search_friends["HeadImgUrl"]
        search_friends_dict["Uin"] = search_friends["Uin"]
        search_friends_dict["Alias"] = search_friends["Alias"]
    print "###search_friends##",search_friends
    return search_friends_dict


def sql_search_class_id(class_info_lsit):
    for i in class_info_lsit:
        service_index.sql_search_class_id(class_info_lsit=class_info_lsit)


def sql_search_user(userName=None, Alias=None, DisplayName=None, Uin=None, keyword=None):
    """
    查询库user表
    :param userName:
    :param Alias:
    :param DisplayName:
    :param Uin:
    :param keyword:
    :return:
    """
    user_list = []
    if userName:
        user_list = service_index.sql_search_user_by_username(user_name=userName)
    if Alias:
        if Alias == "not_Alias_to_key_word" and keyword:
            user_list = service_index.sql_search_user_by_alias(weixin=keyword)
        else:
            user_list = service_index.sql_search_user_by_alias(weixin=Alias)

    return user_list


def q_isat_into(new_instance_b, msg):
    print "######msg#####",msg
    info = msg['Content']
    content = info.replace(msg["jiqiren_name"], "", 1)
    print "content", content
    q_username = msg['FromUserName']
    actual_nick_name = msg['ActualNickName']
    print "q_username", q_username
    print "ActualNickName", actual_nick_name  # 发起用户在群里的昵称

    """获取群成员列表"""
    memberlist = new_instance_b.update_chatroom(q_username, detailedMember=True)

    """更新群成员"""
    school_class_id = service_index.into_q_memberlist(new_instance_b, memberlist)
    print "=======更新群成员=============="
    print "====school_class_id====", school_class_id

    """判断用户角色/修改用户角色"""
    user_list = update_user_role.sql_search_user_role(school_class_id)

    return ""


def into_edu_school_notice(content, to_user_name, user_list, content_class_name=None):
    """
    存储发送内容
    :param content: 内容
    :param to_user_name: 发送者
    :param user_list:
    :param content_class_name:
    :return:
    """
    notice_info_list = []
    if user_list:
        for user in user_list:
            print "#####user.displayname####",user.displayname
            if user.displayname[-2:] == u"老师":
                print "########是老师"
                notice_info = service_index.into_edu_school_notice2(content=content, to_user_name=to_user_name, user=user,
                                                                    content_class_name=content_class_name)
                if notice_info:
                    notice_info_list.append(notice_info)

    return notice_info_list


def q_into_text(new_instance_b, msg):

    print "=====FromUserName===ActualUserName======="
    print msg['FromUserName'], msg['ActualUserName']
    q_username = msg['FromUserName']  # 机器人自己发消息,q_username为ToUserName
    u_username = msg['ActualUserName']  # 发消息的人的信息,q_username为ToUserName
    qun_class = new_instance_b.search_chatrooms(userName=q_username)
    u_user = new_instance_b.search_friends(userName=u_username)
    print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ'
    print u_user
    print u_user["NickName"]
    print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQ'

    """获取微信头像存入数据库"""
    try:
        avatar = new_instance_b.get_head_img(userName=u_username, chatroomUserName=q_username)
    except:
        avatar = ''
    head_img = itchat_upload_images_to_oss(avatar)
    print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
    print "============qun_class================="
    print qun_class
    print "============qun_class================="
    try:
        room_uin = qun_class['Uin']
    except Exception as e:
        room_uin = ''

    try:
        EncryChatRoomId = qun_class['EncryChatRoomId']
    except Exception as e:
        EncryChatRoomId = ''

    try:
        IsOwner = qun_class['IsOwner']
    except Exception as e:
        IsOwner = ''


    data = dict()
    data["content"] = msg['Content']
    data["actual_nick_name"] = msg['ActualNickName']
    data["actual_user_name"] = msg['ActualUserName']
    data["room_uin"] = room_uin
    data["room_user_name"] = q_username
    data["room_nick_name"] = qun_class["NickName"]
    data["msg_type"] = msg['Type']
    data["key_word"] = msg['Url']

    data["city"] = qun_class['City']
    data["province"] = qun_class['Province']
    data["member_count"] = qun_class['MemberCount']
    data["encry_chat_room_id"] = EncryChatRoomId
    data["is_owner"] = IsOwner
    data["robot_uin"] = msg["jiqiren_uin"]
    data["robot_nick_name"] = msg["jiqiren_name"]
    #data["from_uin"] = u_user["Uin"]
    data["from_nick_name"] = u_user["NickName"]
    data["from_user_name"] = msg['ActualNickName']
    data["head_img"] = head_img

    chat_room_data = service_index.into_chat_room_data(data)


from datetime import datetime
# def friend_into_text(msg):
#     print "####msg#####", msg
#     content = msg['Content']
#     from_user_name = msg['FromUserName']
#     to_user_name = msg['ToUserName']
#     print "FromUserName@@@", from_user_name
#     print "ToUserName@@@", to_user_name
#     print "content@@@", content
#     return service_index.into_friend_data_text(content=content, from_user_name=from_user_name,
#                                                   to_user_name=to_user_name)


def friend_into_text2(jqr, content, to_user_name, search_friend, msg_type, created_time=None):
    if created_time is None:
        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_id = service_index.into_friend_data_text2(jqr=jqr, content=content, to_user_name=to_user_name, search_friend=search_friend,
                                                   msg_type=msg_type, created_time=created_time)
    return data_id


def handel_class_update_sys(uin, nick_name, user_name,KeyWord):
    service_index.index_class_update_sys(uin=uin, nick_name=nick_name, user_name=user_name, KeyWord=KeyWord)


def friend_update_sys(uin, nick_name, alias, user_name):
    service_index.friend_update_sys(uin=uin, nick_name=nick_name, alias=alias, user_name=user_name)


def class_manage(new_instance_b, msg, content_name, content_cmd):
    content = msg['Content']
    from_user_name = msg['FromUserName']
    to_user_name = msg['ToUserName']
    friends_info = new_instance_b.search_friends(name=None, userName=from_user_name, remarkName=None, nickName=None)
    # print "#######friends_info##############",friends_info
    friend_uin = friends_info["Uin"]
    friend_nick_name = friends_info["NickName"]
    friend_user_name = friends_info["UserName"]
    weixin = friends_info["Alias"]
    q_class_id_list, q_class_list, q_class_user_name_list, notice_id, error_info = service_index.get_class_id(alias=weixin,
                                                                                                              nick_name=friend_nick_name,
                                                                                                              from_user_name=from_user_name,
                                                                                                              content=content,
                                                                                                              content_name=content_name
                                                                                                              )
    q_class_user_name_list = list(set(q_class_user_name_list))
    bjgl_dict = {"notice_id": notice_id, "Alias": weixin, "nick_name": friend_nick_name, "user_name": friend_user_name,
                 "class_id_list": q_class_id_list, "q_class_user_name_list": q_class_user_name_list,
                 "error_info": error_info}

    return bjgl_dict


# """更新数据， 暂时不用"""
# def into_edu_wx_robot_friend(recod):
#     itchat_get_friends = recod.get_friends()
#     #print "#itchat_get_friends##",itchat_get_friends
#     if itchat_get_friends:
#         service_index.into_edu_wx_robot_friend(itchat_get_friends)
#
#
# """更新数据， 暂时不用"""
# def into_edu_wx_robot_chat(recod):
#     itchat_get_chatrooms = recod.get_chatrooms()
#     #print "#itchat_get_chatrooms##",itchat_get_chatrooms
#     if itchat_get_chatrooms:
#         service_index.into_edu_wx_robot_chat(itchat_get_chatrooms)


    # friend_data_text = index.into_friend_data_text(content=content, from_user_name=from_user_name,
    #                                                to_user_name=to_user_name)
    # content = msg['Content']
    # q_username = msg['FromUserName']  # 机器人自己发消息,q_username为ToUserName
    # actual_nick_name = msg['ActualNickName']
    # actual_user_name = msg['ActualUserName']
    # meg_type = msg['Type']
    # chat_room_data = index.into_chat_room_data(content=content, actual_nick_name=actual_nick_name,
    #                                            actual_user_name=actual_user_name, q_username=q_username)


def find_class_data(school_class_id):
    return dao_find.find_class_user_by_id(school_class_id)


# @cry.task
# def add_friend_chat():
#     return into_edu_wx_robot_friend()
#
#
# @cry.task
# def add_room_chat():
#     return into_edu_wx_robot_chat()


@cry.task
def sync_friends_queue(data):
    print "=======sync_friends_queue=========="
    dao_add.add_edu_friend_data(data)


def sync_friends(recond, friends, jqr):
    print "=======sync_friends=========="
    dao_sql.insert_robot_friend_history(jqr["jqr_uin"])

    for friend in friends:
        """获取微信头像存入数据库"""
        avatar = recond.get_head_img(userName=friend["UserName"])
        head_img = itchat_upload_images_to_oss(avatar)

        if not friend["Alias"]:
            s_friend = recond.search_friends(userName=friend["UserName"])

        data = dict()
        data["robot_uin"] = jqr["jqr_uin"]
        data["robot_nick_name"] = jqr["jqr_name"]
        data["user_name"] = friend["Alias"]
        data["friend_uin"] = friend["Uin"]
        data["nick_name"] = friend["NickName"]
        data["head_img"] = head_img
        data["remark_name"] = friend["DisplayName"]
        data["sex"] = friend["Sex"]
        data["province"] = friend["Province"]
        data["city"] = friend["City"]
        sync_friends_queue.delay(data)


@cry.task
def sync_rooms_member_queue(data):
    print "=======add_edu_robot_room_member_data=========="
    dao_add.add_edu_robot_room_member_data(data)


def sync_rooms(new_instance_b, itchat_get_chatrooms, jqr):
    dao_sql.insert_robot_chat_room_history(jqr["jqr_uin"])
    dao_sql.insert_robot_room_memeber_history()
    for robot in itchat_get_chatrooms:
        print "=====robot itchat_get_chatrooms=========="
        print robot
        if "ChatRoomOwner" in robot:
            ChatRoomOwner = robot["ChatRoomOwner"]
        else:
            ChatRoomOwner = ""

        if "@@" in robot["UserName"] and "NickName" in robot and "Uin" in robot:
            data = dict()
            data["robot_uin"] = jqr["jqr_uin"]
            data["robot_nick_name"] = jqr["jqr_name"]
            data["room_user_name"] = robot["Alias"]
            data["room_uin"] = robot['Uin']
            data["room_nick_name"] = robot["NickName"]
            data["is_owner"] = ChatRoomOwner
            data["encry_chat_room_id"] = robot['EncryChatRoomId']
            data["city"] = robot["City"]
            data["member_count"] = robot["MemberCount"]
            data["province"] = robot["Province"]
            room_id = dao_add.add_edu_robot_room_data(data)

            if robot["MemberList"]:
                print "#####MemberList######", robot["MemberList"]
                for user in robot["MemberList"]:
                    user_info = new_instance_b.search_friends(userName=user["UserName"])
                    if user_info:
                        user_uin = user_info["Uin"]
                    else:
                        user_info = {}
                        user_uin = U'暂无法获取'
                        user_info["NickName"] = user["NickName"]
                    if not user["DisplayName"]:
                        user["DisplayName"] = user_info["NickName"]
                    data = dict()
                    data["room_id"] = room_id
                    data["room_uin"] = robot['Uin']
                    data["member_uin"] = user_uin
                    data["user_name"] = user_info["NickName"]
                    data["room_nick_name"] = robot["NickName"]
                    data["nick_name"] = user["DisplayName"]
                    data["attr_status"] = user["AttrStatus"]
                    data["key_word"] = user["KeyWord"]
                    sync_rooms_member_queue.delay(data)


@cry.task
def sync_data(n):
    for i in range(n):
        print "==================sync_data==msg================"
        print i


@cry.task
def sync_robot_data():
    if len(rts) > 0:
        for robot in rts:
            data = dict()
            data["user_name"] = robot["nick_name"]
            data["nick_name"] = robot["nick_name"]
            data["robot_uin"] = robot["robot_uin"]
            r = dao_find.find_edu_robot_by_uin(robot["robot_uin"])
            if r:
                robot_id = dao_find.update_edu_robot(data, r.id, ["user_name", "nick_name"])
            else:
                robot_id = dao_add.add_edu_robot_data(data)
            print "===sync_robot_data======", robot_id


def add_robot_self(nick_name, uin):
    data = dict()
    data["user_name"] = nick_name
    data["nick_name"] = nick_name
    data["robot_uin"] = uin
    r = dao_find.find_edu_robot_by_uin(uin)
    if r:
        robot_id = dao_find.update_edu_robot(data, r.id, ["user_name", "nick_name"])
    else:
        robot_id = dao_add.add_edu_robot_data(data)
    return robot_id


def service_search_room_id_by_uin(room_uin):
    return dao_find.find_room_by_room_uin(room_uin)


def service_search_room_id_by_nick_name(room_nick_name):
    return dao_find.find_room_by_room_nick_name(room_nick_name)
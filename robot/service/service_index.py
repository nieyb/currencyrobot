# -*- coding:utf-8 -*-
import os, sys, uuid, itchat

import datetime, json

# basedir = os.path.abspath(".")
# print basedir
# sys.path.append(basedir)
from robot.models import DBSession,  Edu_School_Class, Edu_School_Class_User, Edu_School_Notice, \
    EduWxRobotChatRoomData, EduWxRobotChatFriendData,EduWxRobotFriend,EduWxRobotChatRoom,EduWxRobotChatRoomMember,\
    EduWxRobotFriendHistory, EduWxRobotChatRoomFiles
# from config import jiqiren_alias, jiqiren_name

from robot.dao import dao_find, dao_sql, dao_add


def sql_search_user_by_username(user_name):
    user_list = dao_find.find_class_user_by_user_name(user_name)
    if not user_list:
        user_list = []
    return user_list


def sql_search_user_by_alias(weixin):
    user_list = dao_find.find_class_user_by_weixin(weixin)
    if not user_list:
        user_list = []
    return user_list


def get_class_id(alias, nick_name, from_user_name, content,content_name):
    error_info = []
    session = DBSession()
    q_class_id_list = []
    q_class_user_name_list = []
    q_class_list = []
    select_class_id_list = None
    ewrcrd2_notice_id = ""
    if content_name:  # 是否制定班级名称
        select_class_id_list = dao_find.find_school_class_by_name(content_name)

    if select_class_id_list:
        school_class_id = select_class_id_list[0].school_class_id
        if alias:
            print "####alias####", alias
            q_user_all = dao_find.find_school_class_user_by_weixin_and_school_class_id(alias, school_class_id)
            # q_user_all = session.query(Edu_School_Class_User).filter_by(weixin=alias).filter_by(weixin=alias,school_class_id=school_class_id).order_by(Edu_School_Class_User.school_class_id.desc()).all()
        elif from_user_name:
            #q_user_all = session.query(Edu_School_Class_User).filter_by(user_name=from_user_name,school_class_id=school_class_id).order_by(Edu_School_Class_User.school_class_id.desc()).all()
            q_user_all = dao_find.find_school_class_user_by_user_name_and_id(from_user_name, school_class_id)
            if not q_user_all:
                #q_user_all = session.query(Edu_School_Class_User).filter_by(nick_name=nick_name,school_class_id=school_class_id).order_by(Edu_School_Class_User.school_class_id.desc()).all()
                q_user_all = dao_find.find_school_class_user_by_nick_name_and_id(nick_name, school_class_id)
        elif nick_name:
            #q_user_all = session.query(Edu_School_Class_User).filter_by(nick_name=nick_name,school_class_id=school_class_id).order_by(Edu_School_Class_User.school_class_id.desc()).all()
            q_user_all = dao_find.find_school_class_user_by_nick_name_and_id(nick_name, school_class_id)
    else:
        if alias:
            print "####alias####", alias
            #q_user_all = session.query(Edu_School_Class_User).filter_by(weixin=alias).order_by(Edu_School_Class_User.school_class_id.desc()).all()
            q_user_all = dao_find.find_class_user_by_weixin(alias)
        elif from_user_name:
            #q_user_all = session.query(Edu_School_Class_User).filter_by(user_name=from_user_name).order_by(Edu_School_Class_User.school_class_id.desc()).all()
            q_user_all = dao_find.find_class_user_by_user_name(from_user_name)
            if not q_user_all:
                #q_user_all = session.query(Edu_School_Class_User).filter_by(nick_name=nick_name).order_by(Edu_School_Class_User.school_class_id.desc()).all()
                q_user_all = dao_find.find_school_class_user_by_nick_name(nick_name)
        elif nick_name:
            #q_user_all = session.query(Edu_School_Class_User).filter_by(nick_name=nick_name).order_by(Edu_School_Class_User.school_class_id.desc()).all()
            q_user_all = dao_find.find_school_class_user_by_nick_name(nick_name)

    if q_user_all:
        for q_user in q_user_all:
            q_user_displayname = q_user.displayname
            if q_user_displayname[-2:] == u"老师":
                print u"q_user是老师", q_user_displayname, q_user.school_class_id
                q_class_list.append(q_user)
                q_class_id_list.append(q_user.school_class_id)
                #q_class = session.query(Edu_School_Class).filter_by(school_class_id=q_user.school_class_id).first()
                q_class = dao_find.find_school_class_by_id(q_user.school_class_id)
                if q_class:
                    print "##q_class.school_class_name####", q_class.school_class_name
                    q_class_info = itchat.search_chatrooms(name=q_class.school_class_name)
                    if q_class_info:
                        q_class_info = q_class_info[0]
                        q_class_user_name_list.append(q_class_info["UserName"])
                        q_class.user_name = q_class_info["UserName"]
                        ewrcrd2 = Edu_School_Notice(from_id=q_user.user_id, school_class_id=q_user.school_class_id,
                                                    content=content, msg_type=0)
                        session.add(q_class)
                        session.add(ewrcrd2)
                        session.commit()
                        ewrcrd2_notice_id = ewrcrd2.notice_id
                    else:
                        error_info.append("q_class_info_error")
                        # print "q_class_info####", q_class_info

    session.close()
    print "######q_class_id_list######",q_class_id_list
    return q_class_id_list, q_class_list, q_class_user_name_list, ewrcrd2_notice_id, error_info


def into_q_memberlist(new_instance_b, memberlist):
    print "##memberlist#", memberlist
    no_alias_list = []  # 没有微信号用户列表
    # invite_code = uuid.uuid1()
    own_user_Alias=""
    own_user_AttrStatus=""
    own_user_NickName=""
    user_list = memberlist["MemberList"]
    q_username = memberlist["UserName"]
    uin = memberlist["Uin"]
    EncryChatRoomId = memberlist["EncryChatRoomId"]

    """获取当前群信息"""
    xcv = new_instance_b.update_chatroom(userName=EncryChatRoomId)

    KeyWord=xcv["KeyWord"]
    print "########KeyWord#######",KeyWord
    KeyWord = KeyWord
    print "###qun_uin###", uin
    self_user = memberlist["self"]
    chatroomowner = ""

    if "ChatRoomOwner" in memberlist:
        print "%%%%%%%%%%%%%%@@@@@@@@@@@@@", memberlist["ChatRoomOwner"]
        chatroomowner = memberlist["ChatRoomOwner"]

        """获取群创建者信息"""
        own_user = new_instance_b.search_friends(userName=chatroomowner)

        print "own_userown_userown_user@@@@@@@@@@@", own_user["Alias"], own_user["AttrStatus"], own_user["NickName"]
        own_user_Alias=own_user["Alias"]
        own_user_AttrStatus=own_user["AttrStatus"]
        own_user_NickName=own_user["NickName"]
    else:
        print "%%%%%%%%%%%%%%@@@@@@@@@@@@@"

    # chatroomowner = memberlist["ChatRoomOwner"]  # 房间创建者的user_name_id
      # 房间创建者的user_name_id
    q_nickname = memberlist["NickName"]

    if uin and uin != 0 and uin != "0":
        q_ = dao_find.find_school_class_by_uin(uin)
    else:
        q_ = dao_find.find_school_class_by_group_id(q_username)

    if not q_:
        # q_ = dao_base.find_school_class_by_org_id(KeyWord)
        q_ = dao_find.find_school_class_by_org_id_nick_name(KeyWord, q_nickname)
    session = DBSession()
    if not q_:
        data = dict()
        data['group_id'] = q_username
        data['uin'] = uin
        data['chatroomowner'] = chatroomowner
        data['org_id'] = KeyWord
        data['school_class_name'] = q_nickname
        data['invite_code'] = json.dumps({"Alias": own_user_Alias, "AttrStatus": own_user_AttrStatus,
                                          "NickName": own_user_NickName})

        q_ = Edu_School_Class(group_id=q_username, uin=uin, chatroomowner=chatroomowner, org_id=KeyWord,
                              school_class_name=q_nickname,
                              invite_code=json.dumps({"Alias": own_user_Alias,
                                                      "AttrStatus": own_user_AttrStatus,
                                                      "NickName": own_user_NickName}))
        session.add(q_)
        session.commit()

    if q_username:
        q_.group_id = q_username
    if uin and len(uin) >= 3:
        q_.uin = uin
    if chatroomowner:
        q_.chatroomowner = chatroomowner
    if q_nickname:
        q_.school_class_name = q_nickname
    q_.invite_code = json.dumps({"Alias": own_user_Alias, "AttrStatus": own_user_AttrStatus, "NickName": own_user_NickName})
    q_.org_id = KeyWord
    q_.chatroomowner = chatroomowner

    session.add(q_)
    session.commit()
    school_class_id = q_.school_class_id
    session.close()
    for i in user_list:
        if i["Alias"]:
            print "####Alias####", i["Alias"]
        else:
            print "####notAlias ####", i
        q_user = None
        username = i["UserName"]  # userid
        nickname = i["NickName"]  # 昵称
        displayname = i["DisplayName"]  # 群昵称
        alias = i["Alias"]  # 微信号
        province = i["Province"]  # 省份
        city = i["City"]  # 城市
        sex = i["Sex"]  # 性别
        signature = i["Signature"]  # 签名
        KeyWord = i["KeyWord"]  # 关键字
        #headimgurl = i["HeadImgUrl"]  # 头像地址
        headimgurl = ""  # 头像地址
        from robot.util.oss import itchat_upload_images_to_oss
        if username:
            """获取微信头像存入数据库"""
            avatar = new_instance_b.get_head_img(userName=username)
            headimgurl = itchat_upload_images_to_oss(avatar)

        session = DBSession()
        if alias:
            q_user = session.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id).filter_by(weixin=alias).first()
            #q_user = dao_base.find_school_class_user_by_weixin_and_class_id(alias, school_class_id)
            if q_user:
                q_user.displayname = displayname
                q_user.nickname = nickname
                q_user.username = username
                q_user.headimgurl = headimgurl
                q_user.signature = signature
                session.add(q_user)
                session.commit()
            elif displayname:
                q_user = session.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id).filter_by(displayname=displayname).first()
                #q_user = dao_base.find_school_class_user_by_displayname_and_class_id(displayname, school_class_id)
                if q_user:
                    q_user.weixin = alias
                    q_user.nickname = nickname
                    q_user.username = username
                    q_user.headimgurl = headimgurl
                    q_user.signature = signature
                    session.add(q_user)
                    session.commit()
            else:
                #当群用户没修改群昵称时
                q_user = Edu_School_Class_User(user_name=username, headimgurl=headimgurl, displayname=displayname,
                                           weixin=alias, signature=signature, school_class_id=school_class_id,
                                           province=province, city=city, sex=sex, nick_name=nickname)
                session.add(q_user)
                session.commit()
        elif displayname:
            q_user = session.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id).filter_by(displayname=displayname).first()
            #q_user = dao_base.find_school_class_user_by_displayname_and_class_id(displayname, school_class_id)
            if q_user:
                if KeyWord:
                    q_user.weixin = KeyWord
                q_user.username = username
                q_user.headimgurl = headimgurl
                q_user.signature = signature
                session.add(q_user)
                session.commit()
        else:
            q_user = None  # 没有设置微信号
            no_alias_list.append({"username": username, "nickname": nickname, "displayname": displayname})
        if not q_user and displayname:
            q_user = Edu_School_Class_User(user_name=username, headimgurl=headimgurl, displayname=displayname,
                                           weixin=alias, signature=signature, school_class_id=school_class_id,
                                           province=province, city=city, sex=sex, nick_name=nickname)
            session.add(q_user)
            session.commit()
        if q_user and q_user != "error":
            q_user.username = username
            q_user.nickname = nickname
            q_user.headimgurl = headimgurl
            q_user.displayname = displayname
            q_user.alias = alias
            q_user.province = province
            q_user.sex = sex
            q_user.headimgurl = ""
            q_user.signature = signature
            session.add(q_user)
            session.commit()
        session.close()
    return school_class_id
    # # 创建session对象:


def into_edu_school_notice(content, actual_nick_name, actual_user_name, q_username, meg_type):
    session = DBSession()
    esc = dao_find.find_class_by_group_id(q_username)
    escu = dao_find.find_school_class_user_by_user_id(actual_user_name)
    esc_id, escu_id = 0, 0
    if esc:
        esc_id = esc.school_class_id
    if escu:
        escu_id = escu.user_id
    esn = Edu_School_Notice(from_id=escu_id, school_class_id=esc_id, content=content, msg_type="Text")
    session.add(esn)
    session.commit()
    esn_id = esn.notice_id
    session.close()
    return esn_id


def into_chat_room_data(data):
    session = DBSession()
    room_uin = data["room_uin"]
    room_id = 0
    if room_uin:
        print "if room-uin===================="
        print "=room-uin=", room_uin
        room = dao_find.find_room_by_room_uin(room_uin)
        print "====room===="
        print room
        if room:
            print "room_id=", room.id
            room_id = room.id
        # else:
        #     room_id = dao_add.add_edu_robot_room_data(data)
    elif data["room_nick_name"]:
        print "if room_nick_name====================", data["room_nick_name"]
        room = dao_find.find_room_by_room_nick_name(data["room_nick_name"])
        print room
        if room:
            room_id = room.id
        # else:
        #     room_id = dao_add.add_edu_robot_room_data(data)
    print "=============群聊天信息存入数据库============="
    dataa = dict()
    dataa["room_id"] = room_id
    dataa["room_uin"] = room_uin
    dataa["room_user_name"] = data["room_user_name"]
    dataa["content"] = data["content"]
    dataa["msg_type"] = data["msg_type"]
    dataa["room_nick_name"] = data["room_nick_name"]
    dataa["from_user_name"] = data["from_user_name"]
    dataa["from_nick_name"] = data["from_nick_name"]
    dataa["head_img"] = data["head_img"]

    robot_id = dao_add.add_edu_robot_room_chat_data(dataa)


def into_friend_data_text2(jqr, content, to_user_name, search_friend, msg_type, created_time=None):
    session = DBSession()
    if search_friend["Alias"]:
        Alias = search_friend["Alias"]
    else:
        Alias = search_friend["Uin"]
    type_list = [u'Picture', u'Recording', u'Attachment', u'Video']
    if msg_type in type_list:
        msg_type = msg_type
    else:
        msg_type = "text"

    data = dict()
    data["robot_uin"] = jqr["jqr_uin"]
    data["robot_user_name"] = to_user_name
    data["content"] = content
    data["robot_nick_name"] = jqr["jqr_name"]
    data["friend_user_name"] = Alias
    data["friend_uin"] = Alias
    data["friend_nick_name"] = Alias
    data["msg_type"] = msg_type
    data["created_time"] = created_time
    return dao_add.add_friend_chat_data(data)


def search_chatrooms(name=None, userName=None):
    class_info_lsit = []
    if name:
        class_infos = itchat.search_chatrooms(name=name)
        if class_infos:
            for class_info in class_infos:
                class_info_dict ={}
                class_info_dict["UserName"] = class_info["UserName"]
                class_info_dict["MemberList"] = class_info["MemberList"]
                class_info_dict["ChatRoomOwner"] = class_info["ChatRoomOwner"]
                class_info_dict["MemberCount"] = class_info["MemberCount"]
                class_info_dict["NickName"] = class_info["NickName"]
                class_info_dict["self"] = class_info["self"]
                class_info_dict["HeadImgUrl"] = class_info["HeadImgUrl"]
                class_info_lsit.append(class_info_dict)
    return class_info_lsit


def sql_select_class(content_class_name=None,school_class_id=None):  #
    session = DBSession()
    class_sql_obj = None
    if content_class_name:
        class_sql_obj = dao_find.find_school_class_by_class_name(content_class_name)
    elif school_class_id:
        class_sql_obj = dao_find.find_school_class_by_id(school_class_id)
    session.close()
    return class_sql_obj


def into_edu_school_notice2(content,to_user_name, user,content_class_name=None):
    school_class_id = None
    class_sql_obj_by_name = sql_select_class(content_class_name=content_class_name)
    class_sql_obj_by_id = sql_select_class(school_class_id=user.school_class_id)
    if content_class_name and class_sql_obj_by_name:
        if class_sql_obj_by_name.school_class_id == user.school_class_id:
            school_class_id = user.school_class_id
            print u"##班级id相等##",school_class_id
    else:
        school_class_id = user.school_class_id
    if not school_class_id:
        return None
    notice_info = {}
    data = dict()
    data["from_id"] = user.user_id
    data["school_class_id"] = school_class_id
    data["content"] = content
    data["to_id"] = to_user_name
    data["msg_type"] = "text"

    # session = DBSession()
    # esn = Edu_School_Notice(from_id=user.user_id, school_class_id=school_class_id, content=content,to_id=to_user_name,
    #                         msg_type="text")
    # session.add(esn)
    # session.commit()
    # notice_id = esn.notice_id
    # session.close()

    notice_id = dao_add.add_school_notice_data(data)
    search_chatrooms(name=None)
    notice_info["notice_id"] = notice_id
    notice_info["school_class_id"] = user.school_class_id
    notice_info["from_id"] = user.user_id
    notice_info["content"] = content
    notice_info["user_displayname"] = user.displayname

    if class_sql_obj_by_id:
        notice_info["school_class_name"] = class_sql_obj_by_id.school_class_name
        notice_info["school_class_user_name"] = class_sql_obj_by_id.group_id
    else:
        notice_info["school_class_name"] = "---"
        notice_info["school_class_user_name"] = None
    return notice_info


def index_class_update_sys(uin, nick_name, user_name, KeyWord):
    session = DBSession()
    q_class = dao_find.find_school_class_by_uin(uin)
    if q_class:
        q_class.uin = uin
        q_class.nick_name = nick_name
        q_class.user_name = user_name
        q_class.org_id = KeyWord
        session.add(q_class)
        session.commit()
    else:
        q_class = dao_find.find_school_class_by_org_id_nick_name(KeyWord, nick_name)
        if q_class:
            if not q_class.uin:
                q_class.uin = uin
                q_class.nick_name = nick_name
                q_class.user_name = user_name
                q_class.org_id = KeyWord
                session.add(q_class)
                session.commit()
        else:
            q_class = Edu_School_Class(group_id=user_name, uin=uin, chatroomowner="", org_id=KeyWord,
                                       school_class_name=nick_name)
            session.add(q_class)
            session.commit()
    session.close()


def friend_update_sys(uin, nick_name, alias, user_name):
    session = DBSession()
    friend_all = dao_find.find_class_user_by_weixin(str(alias))
    if friend_all:
        print "friend_all###", friend_all
        for friend in friend_all:
            friend.uin = uin
            friend.nick_name = nick_name
            friend.user_name = user_name
            session.add(friend)
            session.commit()
    else:
        print "alias", alias
        friend = Edu_School_Class_User(user_name=user_name, headimgurl="", displayname="", uid=uin, weixin=alias,
                                       signature="", school_class_id=0, province="", city="", sex=0,
                                       nick_name=nick_name)
        session.add(friend)
        session.commit()
    session.close()


# """更新数据， 暂时不用"""
# def into_edu_wx_robot_friend(itchat_get_friends):
#
#     dao_sql.insert_robot_friend_history(jiqiren_alias)
#
#     from robot.util.oss import itchat_upload_images_to_oss
#     for friend in itchat_get_friends:
#
#         """获取微信头像存入数据库"""
#         #avatar = itchat.get_head_img(userName=friend["UserName"])
#         #head_img = itchat_upload_images_to_oss(avatar)
#
#         if not friend["Alias"]:
#             s_friend = itchat.search_friends(userName=friend["UserName"])
#
#         data = dict()
#         data["robot_uin"] = jiqiren_alias
#         data["robot_nick_name"] = jiqiren_name
#         data["user_name"] = friend["Alias"]
#         data["friend_uin"] = friend["Uin"]
#         data["nick_name"] = friend["NickName"]
#         data["head_img"] = ""
#         data["remark_name"] = friend["DisplayName"]
#         data["sex"] = friend["Sex"]
#         data["province"] = friend["Province"]
#         data["city"] = friend["City"]
#         dao_add.add_edu_friend_data(data)

#
# """更新数据， 暂时不用"""
# def into_edu_wx_robot_chat(itchat_get_chatrooms):
#     session = DBSession()
#     # print "############itchat_get_chatrooms",itchat_get_chatrooms
#     session.execute("insert into edu_wx_robot_chat_room_history "
#                     "(room_id,room_uin,robot_uin,robot_user_name,robot_nick_name,encry_chat_room_id,room_user_name,room_nick_name,member_count,province,city)"
#                  "  select id,room_uin,robot_uin,robot_user_name,robot_nick_name,encry_chat_room_id,room_user_name,room_nick_name,member_count,province,city from edu_wx_robot_chat_room")
#     session.commit()
#     del_friend = session.query(EduWxRobotChatRoom).delete()
#     session.commit()
#     session.close()
#     session2 = DBSession()
#     session2.execute("insert into edu_wx_robot_chat_room_member_history "
#             "(member_id,room_id,room_uin,room_nick_name,member_uin,user_name,nick_name,attr_status,key_word,member_status)"
#            "  select id,room_id,room_uin,room_nick_name,member_uin,user_name,nick_name,attr_status,key_word,member_status from edu_wx_robot_chat_room_member")
#     session2.commit()
#     del_friend = session2.query(EduWxRobotChatRoomMember).delete()
#     session2.commit()
#     session2.close()
#     for robot in itchat_get_chatrooms:
#         print "#################robot############",robot
#         session = DBSession()
#         if "ChatRoomOwner" in robot:
#             ChatRoomOwner = robot["ChatRoomOwner"]
#         else:
#             ChatRoomOwner = ""
#         if "@@" in robot["UserName"] and "NickName" in robot and "Uin" in robot:
#             data = dict()
#             data["robot_uin"] = jiqiren_alias
#             data["robot_nick_name"] = jiqiren_alias
#             data["room_user_name"] = robot["Alias"]
#             data["room_uin"] = robot['Uin']
#             data["room_nick_name"] = robot["NickName"]
#             data["is_owner"] = ChatRoomOwner
#             data["encry_chat_room_id"] = ""
#             data["city"] = robot["City"]
#             data["member_count"] = robot["MemberCount"]
#             data["province"] = robot["province"]
#
#             room_id = dao_add.add_edu_robot_room_data(data)
#             if not robot["MemberList"]:
#                 print "#####not MemberList###########", robot
#             if robot["MemberList"]:
#                 print "#####MemberList######", robot["MemberList"]
#                 for user in robot["MemberList"]:
#                     session3 = DBSession()
#                     user_info = itchat.search_friends(userName=user["UserName"])
#                     if user_info:
#                         user_uin = user_info["Uin"]
#                     else:
#                         user_info = {}
#                         user_uin = U'暂无法获取'
#                         user_info["NickName"] = user["NickName"]
#                     if not user["DisplayName"]:
#                         user["DisplayName"] = user_info["NickName"]
#                     new_user2 = EduWxRobotChatRoomMember(room_id=room_id, room_uin=robot['Uin'], member_uin=user_uin,
#                                                          user_name=user_info["NickName"], room_nick_name=robot["NickName"],
#                                                          nick_name=user["DisplayName"], attr_status=user["AttrStatus"],
#                                                          key_word=user["KeyWord"])
#                     session3.add(new_user2)
#                     session3.commit()
#                     session3.close()
#         session.close()

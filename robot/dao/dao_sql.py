# -*- coding:utf-8 -*-

from robot.models import DBSession, EduWxRobotFriend, EduWxRobotChatRoom, EduWxRobotChatRoomMember


def common_insert_data_obj(recond, sql):
    """
    把数据存入历史表， 并删除源表数据
    :param recond: 表类名
    :param sql: sql 语句
    :return:
    """
    session = DBSession()
    session.execute(sql)
    session.commit()
    # session.query(recond).delete()
    # session.commit()
    session.close()


def insert_robot_friend_history(robot_uin):
    """
    好友表历史信息记录
    :return:
    """
    print "==================insert_robot_friend_history==============="
    print robot_uin
    robot_uin = "'"+str(robot_uin) + "'"
    sql_insert = "insert into edu_wx_robot_friend_history (" \
          "friend_id, robot_uin, robot_nick_name, friend_uin, user_name, remark_name, head_img, sex, province, city) " \
          "select id, robot_uin, robot_nick_name, friend_uin, user_name, remark_name, head_img, sex, province, city " \
          "from edu_wx_robot_friend where robot_uin =" + robot_uin

    sql_delete = "delete from edu_wx_robot_friend where robot_uin =" + robot_uin

    common_insert_data_obj(EduWxRobotFriend, sql_insert)
    common_insert_data_obj(EduWxRobotFriend, sql_delete)


def insert_robot_chat_room_history(robot_uin):
    """
    群信息历史记录
    :return:
    """
    robot_uin = "'"+str(robot_uin) + "'"
    sql_insert = "insert into edu_wx_robot_chat_room_history (" \
          "room_id, room_uin, robot_uin, robot_user_name, robot_nick_name, encry_chat_room_id, room_user_name, " \
          "room_nick_name,member_count,province,city) select " \
          "id, room_uin, robot_uin, robot_user_name, robot_nick_name, encry_chat_room_id, room_user_name, " \
          "room_nick_name,member_count,province,city from edu_wx_robot_chat_room where robot_uin=" + robot_uin

    sql_delete = "delete from edu_wx_robot_chat_room where robot_uin =" + robot_uin

    common_insert_data_obj(EduWxRobotChatRoom, sql_insert)
    common_insert_data_obj(EduWxRobotFriend, sql_delete)


def insert_robot_room_memeber_history():
    """
    群成员信息历史记录
    :return:
    """
    sql_insert = "insert into edu_wx_robot_chat_room_member_history (" \
          "member_id, room_id, room_uin, room_nick_name, member_uin, user_name, nick_name, attr_status, " \
          "key_word,member_status) select " \
          "id, room_id, room_uin, room_nick_name, member_uin, user_name, nick_name, attr_status,key_word," \
          "member_status from edu_wx_robot_chat_room_member"

    sql_delete = "delete from edu_wx_robot_chat_room_member"

    common_insert_data_obj(EduWxRobotChatRoomMember, sql_insert)


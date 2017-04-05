# -*- coding:utf-8 -*-

from robot.models import Edu_School_Class, Edu_School_Class_User, Edu_School_Notice, EduWxRobotChatRoomData, \
    EduWxRobotChatFriendData, EduWxRobotFriend, EduWxRobotChatRoom, EduWxRobotChatRoomMember, EduWxRobot, \
    EduWxRobotChatRoomFiles, EduWxRobot

from robot.dao import dao_common as common


def add_friend_chat_data(data):
    ewrc = EduWxRobotChatFriendData()
    common.set_data_to_record(ewrc, data)
    return common.insert_data(ewrc)


def add_edu_friend_data(data):
    friend = EduWxRobotFriend()
    common.set_data_to_record(friend, data)
    return common.insert_data(friend)


def add_room_files_data(data):
    roomfilse = EduWxRobotChatRoomFiles()
    common.set_data_to_record(roomfilse, data)
    return common.insert_data(roomfilse)


def add_school_class_data(data):
    sclass = Edu_School_Class()
    common.set_data_to_record(sclass, data)
    return common.insert_data(sclass)


def add_school_notice_data(data):
    notice = Edu_School_Notice()
    common.set_data_to_record(notice, data)
    return common.insert_data(notice)


def add_edu_robot_data(data):
    robot = EduWxRobot()
    common.set_data_to_record(robot, data)
    return common.insert_data(robot)


def add_edu_robot_room_data(data):
    room = EduWxRobotChatRoom()
    common.set_data_to_record(room, data)
    return common.insert_data(room)


def add_edu_robot_room_member_data(data):
    member = EduWxRobotChatRoomMember()
    common.set_data_to_record(member, data)
    return common.insert_data(member)


def add_edu_robot_room_chat_data(data):
    chat = EduWxRobotChatRoomData()
    common.set_data_to_record(chat, data)
    return common.insert_data(chat)
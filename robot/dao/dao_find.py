# -*- coding:utf-8 -*-

from robot.models import DBSession,  Edu_School_Class, Edu_School_Class_User, Edu_School_Notice, \
    EduWxRobotChatRoomData, EduWxRobotChatFriendData,EduWxRobotFriend,EduWxRobotChatRoom,EduWxRobotChatRoomMember, \
    EduWxRobotChatRoomFiles, EduWxRobot
from robot.dao import dao_common as common


def find_data_by_sql(sql):
    """
    通过sql查询并删除
    :param sql:
    :return:
    """
    son = DBSession()
    son.execute(sql)
    son.commit()
    son.close()
    return


def find_edu_robot_by_uin(robot_uin):
    """
    通过机器人uin查询返回机器人信息
    :param robot_uin:
    :return: object
    """
    son = DBSession()
    ob = son.query(EduWxRobot).filter_by(robot_uin=robot_uin).first()
    son.close()
    return ob


def update_edu_robot(data, record_id, attrs):
    record = EduWxRobot()
    common.set_data_to_record(record, data)
    return common.update_data(record, record_id, attrs)


def find_class_user_by_id(school_class_id):
    """
    通过班级id查询返回所有当前班级用户信息
    :param school_class_id:
    :return: objects
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id).all()
    son.close()
    return obs


def find_class_user_by_user_name(user_name):
    """
    通过用户名称查询返回所有当前班级用户信息
    :param user_name:
    :return: objects
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(user_name=user_name).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_class_user_by_weixin(weixin):
    """
    通过用户微信号查询返回当前班级用户信息
    :param weixin:
    :return: objects
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(weixin=weixin).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_school_class_by_name(school_class_name):
    """

    :param school_class_name:
    :return:
    """
    son = DBSession()
    obs = son.query(Edu_School_Class).filter_by(school_class_name=school_class_name).order_by(
        Edu_School_Class.school_class_id.desc()).all()
    son.close()
    return obs


def find_school_class_by_id(school_class_id):
    """
    通过班级id查询返回当前班级信息
    :param school_class_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(school_class_id=school_class_id).first()
    son.close()
    return ob


def find_school_class_user_by_user_name_and_id(user_name, school_class_id):
    """
    通过发消息老师的name 和所在班级的id返回用户信息
    :param user_name:
    :param school_class_id:
    :return:objects
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(user_name=user_name, school_class_id=school_class_id).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_school_class_user_by_nick_name_and_id(nick_name, school_class_id):
    """
    通过用户nick_name 和所在班级的id返回用户信息
    :param nick_name:
    :param school_class_id:
    :return:object
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(nick_name=nick_name, school_class_id=school_class_id).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_school_class_user_by_nick_name(nick_name):
    """
    通过用户的个人昵称查询返回当前班级的信息
    :param nick_name:
    :return:object
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(nick_name=nick_name).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_class_by_group_id(group_id):
    """
    通过班级group_id查询返回所有当前班级信息
    :param group_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(group_id=group_id).first()
    son.close()
    return ob


def find_school_class_user_by_user_id(user_id):
    """
    通过发起者的user_id查询返回用户信息
    :param user_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class_User).filter_by(user_id=user_id).first()
    son.close()
    return ob


def find_school_class_user_by_weixin_and_school_class_id(weixin, school_class_id):
    """
    通过微信号班级id查询返回用户信息
    :param weixin:
    :param school_class_id:
    :return:object
    """
    son = DBSession()
    obs = son.query(Edu_School_Class_User).filter_by(weixin=weixin,school_class_id=school_class_id).order_by(
        Edu_School_Class_User.school_class_id.desc()).all()
    son.close()
    return obs


def find_school_class_user_by_weixin_and_class_id(weixin, school_class_id):
    """
    通过微信号班级id查询返回单个用户信息
    :param weixin:
    :param school_class_id:
    :return:object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class_User).filter_by(weixin=weixin,school_class_id=school_class_id).first()
    son.close()
    return ob


def find_school_class_user_by_displayname_and_class_id(displayname, school_class_id):
    """
    通过微信号班级id查询返回单个用户信息
    :param displayname:
    :param school_class_id:
    :return:object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class_User).filter_by(displayname=displayname, school_class_id=school_class_id).first()
    son.close()
    return ob


def find_school_class_by_uin(uin):
    """
    通过uin查询返回班级信息
    :param uin:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(uin=uin).first()
    son.close()
    return ob


def find_school_class_by_group_id(group_id):
    """
    通过group_id查询返回班级信息
    :param group_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(group_id=group_id).first()
    son.close()
    return ob


def find_school_class_by_org_id(org_id):
    """
    通过org_id 查询返回班级信息
    :param org_id:
    :return:object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(org_id=org_id).first()
    son.close()
    return ob


def find_school_class_by_org_id_nick_name(org_id, school_class_name):
    """
    通过org_id,nick_name查询返回班级信息
    :param org_id:
    :param nick_name:
    :return:object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(org_id=org_id, school_class_name=school_class_name).first()
    son.close()
    return ob


def find_school_class_by_class_name(school_class_name):
    """
    通过班级名称查询返回班级信息
    :param schoo_class_name:
    :return:object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class).filter_by(school_class_name=school_class_name).order_by(
        Edu_School_Class.school_class_id.desc()).first()
    son.close()
    return ob


def find_class_user_by_user_name_and_class_id(user_name, school_class_id):
    """
    通过姓名和班级id查询返回用户信息
    :param user_name:
    :param school_class_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id, user_name=user_name).first()
    son.close()
    return ob


def find_room_by_room_uin(room_uin):
    """
    通过room_uin查询返回群信息
    :param user_name:
    :param school_class_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(EduWxRobotChatRoom).filter_by(room_uin=room_uin).first()
    son.close()
    return ob


def find_room_by_room_nick_name(room_nick_name):
    """
    通过room_nick_name查询群信息
    :param user_name:
    :param school_class_id:
    :return: object
    """
    son = DBSession()
    ob = son.query(EduWxRobotChatRoom).filter_by(room_nick_name=room_nick_name).first()
    son.close()
    return ob




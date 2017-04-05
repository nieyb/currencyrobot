# -*- coding:utf-8 -*-
import datetime
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import mysql_url
# 创建对象的基类:

Base = declarative_base()

# 初始化数据库连接:('数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名')(引擎包括【mysql-connector，mysqldb】)
engine = db.create_engine(mysql_url)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
conn = engine.connect()


class Edu_School_Class(Base):
    '''学校年级班级表'''
    __tablename__ = 'edu_school_class'
    school_class_id = db.Column(db.Integer, primary_key=True, index=True)
    group_id = db.Column(db.String(100))
    uin = db.Column(db.String(100))
    robot_uin = db.Column(db.String(100))
    chatroomowner = db.Column(db.String(100))
    school_class_name = db.Column(db.String(256))
    status = db.Column(db.Integer, nullable=False, default=0)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    invite_code = db.Column(db.String(255))
    org_id = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class Edu_School_Class_Member(Base):
    '''学校年级班级用户表'''
    __tablename__ = 'edu_school_class_member'
    class_member_id = db.Column(db.Integer, primary_key=True, index=True)
    school_class_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(500))
    user_role = db.Column(db.Integer, nullable=False, default=0)
    org_id = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime)


class Edu_School_Notice(Base):
    '''消息表'''
    __tablename__ = 'edu_school_notice'
    notice_id = db.Column(db.Integer, primary_key=True, index=True)
    from_id = db.Column(db.Integer, nullable=False, default=0)
    school_class_id = db.Column(db.Integer)
    to_id = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    img_url = db.Column(db.String(200))
    msg_type = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    org_id = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime)


class Edu_School_Notice_Detail(Base):
    '''学校年级班级表'''
    __tablename__ = 'edu_school_notice_detail'
    detail_id = db.Column(db.Integer, primary_key=True, index=True)
    notice_id = db.Column(db.Integer)
    school_class_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    from_id = db.Column(db.Integer, nullable=False, default=0)
    to_id = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    img_url = db.Column(db.String(100))
    msg_type = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    org_id = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime,default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime)


class Edu_School_Class_User(Base):
    '''学校年级班级用户表'''
    __tablename__ = 'edu_school_class_user'
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    user_name = db.Column(db.String(100))
    nick_name = db.Column(db.String(100))
    displayname = db.Column(db.String(100))
    uid = db.Column(db.Integer)
    school_class_id = db.Column(db.Integer)
    temporary_user_id = db.Column(db.Integer)
    student_number = db.Column(db.String(100))
    student_card = db.Column(db.String(100))
    student_subject = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    weixin = db.Column(db.String(100))
    weixin_openid = db.Column(db.String(100))
    avatar = db.Column(db.String(200))
    status = db.Column(db.Integer, nullable=False, default=0)
    user_role = db.Column(db.Integer, nullable=False, default=0)
    student_id = db.Column(db.Integer, nullable=False, default=0)

    province = db.Column(db.String(32))
    city = db.Column(db.String(32))
    sex = db.Column(db.String(16))
    headimgurl = db.Column(db.String(512))
    signature = db.Column(db.String(512))

    org_id = db.Column(db.Integer, nullable=False, default=0)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)


class EduWxRobot(Base):
    """机器人信息表"""
    __tablename__ = 'edu_wx_robot'
    id = db.Column(db.Integer, primary_key=True, index=True)
    robot_uin = db.Column(db.String(500))
    user_name = db.Column(db.String(500))
    nick_name = db.Column(db.String(500))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotFriend(Base):
    """机器人好友信息表"""
    __tablename__ = 'edu_wx_robot_friend'
    id = db.Column(db.Integer, primary_key=True, index=True)
    robot_uin = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    friend_uin = db.Column(db.String(500))
    user_name = db.Column(db.String(500))
    nick_name = db.Column(db.String(500))
    remark_name = db.Column(db.String(500))
    head_img = db.Column(db.String(500))
    sex = db.Column(db.String(10))
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotFriendHistory(Base):
    """机器人好友历史信息表"""
    __tablename__ = 'edu_wx_robot_friend_history'
    id = db.Column(db.Integer, primary_key=True, index=True)
    friend_id = db.Column(db.Integer)
    robot_uin = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    friend_uin = db.Column(db.String(500))
    user_name = db.Column(db.String(500))
    nick_name = db.Column(db.String(500))
    remark_name = db.Column(db.String(500))
    head_img = db.Column(db.String(500))
    sex = db.Column(db.String(10))
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)
    import_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotChatRoom(Base):
    """机器人群聊信息表"""
    __tablename__ = 'edu_wx_robot_chat_room'
    id = db.Column(db.Integer, primary_key=True, index=True)
    robot_uin = db.Column(db.String(500))
    robot_user_name = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    room_uin = db.Column(db.String(500))
    is_owner = db.Column(db.String(100))
    is_admin = db.Column(db.String(100))
    admin_user_name = db.Column(db.String(500))
    admin_nick_name = db.Column(db.String(500))
    admin_uin = db.Column(db.String(500))
    encry_chat_room_id = db.Column(db.String(500))
    room_user_name = db.Column(db.String(500))
    room_nick_name = db.Column(db.String(500))
    member_count = db.Column(db.String(100))
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotChatRoomHistory(Base):
    """机器人群聊历史信息表"""
    __tablename__ = 'edu_wx_robot_chat_room_history'
    id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.Integer)
    robot_uin = db.Column(db.String(500))
    robot_user_name = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    room_uin = db.Column(db.String(500))
    is_owner = db.Column(db.String(100))
    is_admin = db.Column(db.String(100))
    admin_user_name = db.Column(db.String(500))
    admin_nick_name = db.Column(db.String(500))
    admin_uin = db.Column(db.String(500))
    encry_chat_room_id = db.Column(db.String(500))
    room_user_name = db.Column(db.String(500))
    room_nick_name = db.Column(db.String(500))
    member_count = db.Column(db.String(100))
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)
    import_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotChatRoomMember(Base):
    """群用户信息表"""
    __tablename__ = 'edu_wx_robot_chat_room_member'
    id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.Integer)
    room_uin = db.Column(db.String(500))
    room_nick_name = db.Column(db.String(500))
    member_uin = db.Column(db.String(500))
    user_name = db.Column(db.String(500))
    nick_name = db.Column(db.String(500))
    attr_status = db.Column(db.String(500))
    key_word = db.Column(db.String(500))
    member_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotChatRoomMemberHistory(Base):
    """群用户历史信息表"""
    __tablename__ = 'edu_wx_robot_chat_room_member_history'
    id = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    room_uin = db.Column(db.String(500))
    room_nick_name = db.Column(db.String(500))
    member_uin = db.Column(db.String(500))
    user_name = db.Column(db.String(500))
    nick_name = db.Column(db.String(500))
    attr_status = db.Column(db.String(500))
    key_word = db.Column(db.String(500))
    member_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.datetime.now)
    import_time = db.Column(db.DateTime, default=datetime.datetime.now)


class EduWxRobotChatRoomData(Base):
    """群聊天记录信息表"""
    __tablename__ = 'edu_wx_robot_chat_room_data'
    id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.Integer)
    room_uin = db.Column(db.String(500))
    room_user_name = db.Column(db.String(500))
    room_nick_name = db.Column(db.String(500))
    from_uin = db.Column(db.String(500))
    from_user_name = db.Column(db.String(500))
    from_nick_name = db.Column(db.String(500))
    msg_type = db.Column(db.String(500))
    key_word = db.Column(db.String(500))
    content = db.Column(db.TEXT)
    head_img = db.Column(db.String(500))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    #updated_time = db.Column(db.DateTime)


class EduWxRobotChatFriendData(Base):
    """好友聊天记录信息表"""
    __tablename__ = 'edu_wx_robot_chat_friend_data'
    id = db.Column(db.Integer, primary_key=True, index=True)
    robot_uin = db.Column(db.String(500))
    robot_user_name = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    friend_uin = db.Column(db.String(500))
    friend_user_name = db.Column(db.String(500))
    friend_nick_name = db.Column(db.String(500))
    msg_type = db.Column(db.String(500))
    key_word = db.Column(db.String(500))
    content = db.Column(db.TEXT)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)



class EduWxRobotChatRoomFiles(Base):
    """群成长信息记录"""
    __tablename__ = 'edu_wx_robot_chat_room_files'
    id = db.Column(db.Integer, primary_key=True, index=True)
    robot_uin = db.Column(db.String(500))
    robot_user_name = db.Column(db.String(500))
    robot_nick_name = db.Column(db.String(500))
    from_uin = db.Column(db.String(500))
    from_user_name = db.Column(db.String(500))
    from_nick_name = db.Column(db.String(500))
    msg_type = db.Column(db.String(500))
    key_word = db.Column(db.String(500))
    content = db.Column(db.TEXT)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
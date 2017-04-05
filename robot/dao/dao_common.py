# -*- coding:utf-8 -*-
import datetime
from sqlalchemy.inspection import inspect
from robot.models import DBSession


def get_pk(record):
    return inspect(record.__class__).primary_key[0].name


def insert_data(record):
    """
    插入记录，并返回id
    :param record: 初始化对象
    :return: id
    :example:
    def add_course_dynamic(data)
        dynamic = EduCourseDynamic()
        set_data_to_record(dynamic, data)
        return insert_data(dynamic)
    """
    son = DBSession()
    son.add(record)
    son.commit()
    record_id = getattr(record, get_pk(record))
    son.close()
    # flog.info("insert a record --" + str(record) + "id--: " + str(record_id))
    print "===========record_id================="
    print record_id
    print "====================================="
    return record_id


def set_data_to_record(record, data):
    """

    :param record: 初始化对象
    :param data: 存储的数据, dict
    :return:
    """
    def _filter_build_in(keys):
        new_keys = list()
        for k in keys:
            if not k.startswith("_"):
                new_keys.append(k)
        return new_keys

    attrs = _filter_build_in(dir(record))

    """将data设置值到record对象中"""
    for key in attrs:
        if key == "created_time":
            data["created_time"] = datetime.datetime.now()

        if data.has_key(key):
            setattr(record, key, data[key])


def update_data(record, record_id, attrs):
    """
    更新记录的attrs字段，不允许为空
    :param record: 已经赋值的对象
    :param record_id: 需要更新的对象主键
    :param attrs: 需要更新的字段名的 list， 如["product_count","product_name"]
    :return:
    """
    son = DBSession()
    # record_id = getattr(record, get_pk(record))
    print "========update_data record_id===========", record_id
    if int(record_id) > 0:
        if len(attrs) == 0:
            return
        update_columns = {}
        for a in attrs:
            update_columns[a] = getattr(record, a)
        if update_columns:
            son.query(record.__class__).filter_by(**{get_pk(record): record_id}).update(update_columns)
            son.commit()
            son.close()
        return record_id
    else:
        return False

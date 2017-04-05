# -*- coding:utf-8 -*-
from robot.models import DBSession, Edu_School_Class_User
from robot.constants import PARENTS
from robot.dao import dao_find

def sql_search_user_role(school_class_id):
    session = DBSession()
    #user_list = session.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id).all()
    user_list = dao_find.find_class_user_by_id(school_class_id)
    session.close()
    if not user_list:
        user_list = []
    else:
        for u in user_list:
            print "=============uuuuuuu================"
            print u
            if u.displayname!=None:
                print "====u.displayname!=None======"
                print u.displayname
                if u'老师' in u.displayname:
                    #user_role = u.user_role
                    if u.user_role !=1:
                        u.user_role=1
                        session.add(u)
                        session.commit()
                for p in PARENTS:
                    if p in u.displayname:
                        student_name = (u.displayname).split(p)[0]
                        #student_user = session.query(Edu_School_Class_User).filter_by(school_class_id=school_class_id, user_name=student_name).first()
                        student_user = dao_find.find_class_user_by_user_name_and_class_id(student_name, school_class_id)
                        if student_user:
                            student_id = student_user.user_id
                        else:
                            student = Edu_School_Class_User(user_name=student_name,school_class_id=school_class_id,user_role=3)
                            session.add(student) #存储学生信息
                            session.commit()
                            student_id = student.user_id
                        u.student_id = student_id #父母存储学生id
                        if u.user_role!=2:
                            u.user_role=2
                        session.add(u)
                        session.commit()



    return user_list
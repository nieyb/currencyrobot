-- --------------------------------------------------------
-- 点滴云SaaS服务平台数据库建库脚本
-- 创建人: nyb
-- 创建时间: 2016-6-30
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出 diandiyun 的数据库结构
DROP DATABASE IF EXISTS `robotcurrency`;
CREATE DATABASE IF NOT EXISTS `robotcurrency` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;
USE `robotcurrency`;


-- 创建  表 diandiyun.edu_school_class 结构
DROP TABLE IF EXISTS `edu_school_class`;
CREATE TABLE `edu_school_class` (
  `school_class_id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `group_id` VARCHAR(100) COMMENT '群user_name_id',
  `uin` VARCHAR(100) COMMENT '群uni_id',
  `robot_uin` VARCHAR(100) COMMENT '机器人uin',
  `chatroomowner` VARCHAR(100) COMMENT '房间创建者的username_id',
  `school_class_name` VARCHAR(100) NOT NULL COMMENT '年级/班级名称',
  `status` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:正常,1:关闭',
  `parent_id` INT(11) unsigned NOT NULL DEFAULT 0 COMMENT '班级属于年级ID，0表示顶级',
  `invite_code` varchar(255) DEFAULT NULL COMMENT '邀请码',
  `org_id` INT(11) NOT NULL COMMENT '机构ID',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',  
  PRIMARY KEY (`school_class_id`)
)
COMMENT='学校年级班级表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
CHARSET=utf8
AUTO_INCREMENT=1000
;

-- 创建  表 diandiyun.edu_school_class_user 结构
DROP TABLE IF EXISTS `edu_school_class_user`;
CREATE TABLE `edu_school_class_user` (
  `user_id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `user_name` VARCHAR(100) COMMENT '名称',
  `nick_name` VARCHAR(100) COMMENT '微信昵称',
  `displayname` VARCHAR(100) COMMENT '微信群昵称',
  `student_number` VARCHAR(100) COMMENT '学号',
  `student_card` VARCHAR(100) COMMENT '学籍卡',
  `student_subject` VARCHAR(100) COMMENT '学科',
  `tel` VARCHAR(20) COMMENT '手机号',
  `weixin` VARCHAR(100) COMMENT '微信号',
  `weixin_openid` VARCHAR(100) COMMENT '微信openid',
  `avatar` VARCHAR(200) COMMENT '头像',
  `uid` VARCHAR(100) COMMENT '微信用户原始的id',
  `school_class_id` int NOT NULL COMMENT '班级id',
  `temporary_user_id` VARCHAR(100) COMMENT '暂定位授课老师名称',
  `status` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:在籍,1:退学，2:休学,3:转学',
  `user_role` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.1:老师，2:家长,3:学生,4: 其他',
  `student_id` INT(11) unsigned NOT NULL DEFAULT 0 COMMENT '学生ID，0表示学生本人',
  `province` VARCHAR(32) COMMENT '省份',
  `city` VARCHAR(32) COMMENT '城市',
  `sex` VARCHAR(16) COMMENT '性别',
  `headimgurl` VARCHAR(128) COMMENT '头像url',
  `signature` VARCHAR(512) COMMENT '签名',
  `org_id` INT(11) NOT NULL COMMENT '机构ID',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`user_id`)
)
COMMENT='学校年级班级用户表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
CHARSET=utf8
AUTO_INCREMENT=1000
;


-- 创建  表 diandiyun.edu_school_class_member 结构
DROP TABLE IF EXISTS `edu_school_class_member`;
CREATE TABLE `edu_school_class_member` (
  `class_member_id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `school_class_id` int NOT NULL COMMENT '班级编号',
  `user_id` int NOT NULL COMMENT '用户ｉｄ',
  `user_name` VARCHAR(100) COMMENT '名称',
  `user_role` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:创建者,1:协同者，2:家长,3:学生, 4: 其他',
  `org_id` INT(11) NOT NULL COMMENT '机构ID',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`class_member_id`)
)
COMMENT='学校年级班级用户关联表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
CHARSET=utf8
AUTO_INCREMENT=1000
;


-- 创建  表 diandiyun.edu_school_class 结构
DROP TABLE IF EXISTS `edu_school_notice`;
CREATE TABLE `edu_school_notice` (
  `notice_id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `from_id` int(10) NOT NULL DEFAULT 0 COMMENT '发布者Id',
  `school_class_id` int NOT NULL COMMENT '班级编号',
  `to_id` text COMMENT '发送对象Id',
  `title` VARCHAR(100) COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `img_url` VARCHAR(200) COMMENT '图片',
  `msg_type` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:图文,1:文本',
  `status` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:正常,1:关闭',
  `org_id` INT(11) NOT NULL COMMENT '机构ID',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',  
  PRIMARY KEY (`notice_id`)
)
COMMENT='发送消息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
CHARSET=utf8
AUTO_INCREMENT=1000
;


-- 创建  表 diandiyun.edu_school_notice_detail 结构
DROP TABLE IF EXISTS `edu_school_notice_detail`;
CREATE TABLE `edu_school_notice_detail` (
  `detail_id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `notice_id` int NOT NULL COMMENT '消息编号',
  `school_class_id` int NOT NULL COMMENT '班级编号',
  `user_id` int NOT NULL COMMENT '学生ｉｄ',
  `title` VARCHAR(100) COMMENT '标题',
  `content` text COMMENT '内容',
  `img_url` VARCHAR(200) COMMENT '图片',
  `from_id` int(10) NOT NULL DEFAULT 0 COMMENT '发布者Id',
  `to_id` text COMMENT '确认者Id',
  `msg_type` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:图文,1:文本',
  `status` tinyint(1) unsigned DEFAULT 0 COMMENT '状态.0:正常,1:关闭',
  `org_id` INT(11) NOT NULL COMMENT '机构ID',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',  
  PRIMARY KEY (`detail_id`)
)
COMMENT='学校家长却认通知表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
CHARSET=utf8
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot 结构
DROP TABLE IF EXISTS `edu_wx_robot`;
CREATE TABLE `edu_wx_robot` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `user_name` VARCHAR(100) COMMENT '键值名称',
  `nick_name` VARCHAR(100) COMMENT '昵称',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`id`)
)
COMMENT='机器人信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_friend 结构
DROP TABLE IF EXISTS `edu_wx_robot_friend`;
CREATE TABLE `edu_wx_robot_friend` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_nick_name` VARCHAR(100) COMMENT '微信ｉｄ',
  `friend_uin` VARCHAR(100) COMMENT '好友微信ｉｄ',
  `user_name` VARCHAR(100) COMMENT '好友键值名称',
  `nick_name` VARCHAR(100) COMMENT '好友昵称',
  `remark_name` VARCHAR(100) COMMENT '备注昵称',
  `head_img` VARCHAR(500) COMMENT '好友头像',
  `sex` VARCHAR(10) COMMENT '性别',
  `province` VARCHAR(10) COMMENT '省份',
  `city` VARCHAR(10) COMMENT '地区',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`id`)
)
COMMENT='机器人好友信息表'
COLLATE='utf8_general_ci'
CHARSET='utf8'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;

-- 创建  表 diandijiaxiao.edu_wx_robot_friend_history 结构
DROP TABLE IF EXISTS `edu_wx_robot_friend_history`;
CREATE TABLE `edu_wx_robot_friend_history` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `friend_id` int NOT NULL COMMENT '原来编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_nick_name` VARCHAR(100) COMMENT '微信ｉｄ',
  `friend_uin` VARCHAR(100) COMMENT '好友微信ｉｄ',
  `user_name` VARCHAR(100) COMMENT '好友键值名称',
  `nick_name` VARCHAR(100) COMMENT '好友昵称',
  `remark_name` VARCHAR(100) COMMENT '备注昵称',
  `head_img` VARCHAR(500) COMMENT '好友头像',
  `sex` VARCHAR(10) COMMENT '性别',
  `province` VARCHAR(10) COMMENT '省份',
  `city` VARCHAR(10) COMMENT '地区',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  `import_time` datetime comment '导入时间',
  PRIMARY KEY (`id`)
)
COMMENT='机器人好友历史信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;

-- 创建  表 diandijiaxiao.edu_wx_robot_chat_room 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room`;
CREATE TABLE `edu_wx_robot_chat_room` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_user_name` VARCHAR(100) COMMENT '微信键值',
  `robot_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `room_uin` VARCHAR(100) COMMENT '微信群ｉｄ',
  `is_owner` VARCHAR(100) COMMENT '',
  `is_admin` VARCHAR(100) COMMENT '',
  `admin_user_name` VARCHAR(100) COMMENT '',
  `admin_nick_name` VARCHAR(100) COMMENT '',
  `admin_uin` VARCHAR(100) COMMENT '',
  `encry_chat_room_id` VARCHAR(100) COMMENT '微信群EncryChatRoomId',
  `room_user_name` VARCHAR(100) COMMENT '微信群值键值',
  `room_nick_name` VARCHAR(100) COMMENT '微信群昵称',
  `member_count` VARCHAR(100) COMMENT '成员总数',
  `province` VARCHAR(100) COMMENT '省份',
  `city` VARCHAR(100) COMMENT '地区',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`id`)
)
COMMENT='机器人群聊信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_room_history 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room_history`;
CREATE TABLE `edu_wx_robot_chat_room_history` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `room_id` int NOT NULL COMMENT '原始编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_user_name` VARCHAR(100) COMMENT '微信键值',
  `robot_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `room_uin` VARCHAR(100) COMMENT '微信群ｉｄ',
  `is_owner` VARCHAR(100) COMMENT '',
  `is_admin` VARCHAR(100) COMMENT '',
  `admin_user_name` VARCHAR(100) COMMENT '',
  `admin_nick_name` VARCHAR(100) COMMENT '',
  `admin_uin` VARCHAR(100) COMMENT '',
  `encry_chat_room_id` VARCHAR(100) COMMENT '微信群EncryChatRoomId',
  `room_user_name` VARCHAR(100) COMMENT '微信群值键值',
  `room_nick_name` VARCHAR(100) COMMENT '微信群昵称',
  `member_count` VARCHAR(100) COMMENT '成员总数',
  `province` VARCHAR(100) COMMENT '省份',
  `city` VARCHAR(100) COMMENT '地区',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  `import_time` datetime comment '导入时间',
  PRIMARY KEY (`id`)
)
COMMENT='机器人群聊历史信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_room_member 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room_member`;
CREATE TABLE `edu_wx_robot_chat_room_member` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `room_id` int NOT NULL COMMENT 'room编号',
  `room_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `room_nick_name` VARCHAR(100) COMMENT '微信ｉｄ',
  `member_uin` VARCHAR(100) COMMENT '成员微信ｉｄ',
  `user_name` VARCHAR(100) COMMENT '键值名称',
  `nick_name` VARCHAR(100) COMMENT '昵称',
  `attr_status` VARCHAR(100) COMMENT '',
  `key_word` VARCHAR(100) COMMENT '关键字',
  `member_status` VARCHAR(100) COMMENT '状态',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  PRIMARY KEY (`id`)
)
COMMENT='群用户信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_room_member_history 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room_member_history`;
CREATE TABLE `edu_wx_robot_chat_room_member_history` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `member_id` int NOT NULL COMMENT 'room_member原始编号',
  `room_id` int NOT NULL COMMENT 'room编号',
  `room_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `room_nick_name` VARCHAR(100) COMMENT '微信ｉｄ',
  `member_uin` VARCHAR(100) COMMENT '成员微信ｉｄ',
  `user_name` VARCHAR(100) COMMENT '键值名称',
  `nick_name` VARCHAR(100) COMMENT '昵称',
  `attr_status` VARCHAR(100) COMMENT '',
  `key_word` VARCHAR(100) COMMENT '关键字',
  `member_status` VARCHAR(100) COMMENT '状态',
  `created_time` datetime comment '创建时间',
  `updated_time` datetime comment '更新时间',
  `import_time` datetime comment '导入时间',
  PRIMARY KEY (`id`)
)
COMMENT='群用户历史信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_room_data 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room_data`;
CREATE TABLE `edu_wx_robot_chat_room_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `room_id` int NOT NULL COMMENT 'room编号',
  `room_uin` VARCHAR(100) COMMENT '微信群ｉｄ',
  `from_uin` VARCHAR(100) COMMENT '发送信息人的id',
  `room_user_name` VARCHAR(100) COMMENT '微信群键值名称',
  `room_nick_name` VARCHAR(100) COMMENT '微信群昵称',
  `from_user_name` VARCHAR(100) COMMENT '发送信息人名称',
  `from_nick_name` VARCHAR(100) COMMENT '发送信息人昵称',
  `head_img` VARCHAR(500) COMMENT '用户头像',
  `msg_type` VARCHAR(100) COMMENT '消息类型',
  `key_word` VARCHAR(100) COMMENT '关键字',
  `content` text COMMENT '内容',
  `send_time` datetime comment '发送时间',
  `created_time` datetime comment '创建时间',
  PRIMARY KEY (`id`)
)
COMMENT='群聊天记录信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_friend_data 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_friend_data`;
CREATE TABLE `edu_wx_robot_chat_friend_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_user_name` VARCHAR(100) COMMENT '微信昵称',
  `robot_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `friend_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `friend_user_name` VARCHAR(100) COMMENT '微信昵称',
  `friend_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `msg_type` VARCHAR(100) COMMENT '消息类型',
  `key_word` VARCHAR(100) COMMENT '关键字',
  `content` text COMMENT '内容',
  `send_time` datetime comment '发送时间',
  `created_time` datetime comment '创建时间',
  PRIMARY KEY (`id`)
)
COMMENT='好友聊天记录信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;


-- 创建  表 diandijiaxiao.edu_wx_robot_chat_friend_data 结构
DROP TABLE IF EXISTS `edu_wx_robot_chat_room_files`;
CREATE TABLE `edu_wx_robot_chat_room_files` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `robot_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `robot_user_name` VARCHAR(100) COMMENT '微信昵称',
  `robot_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `from_uin` VARCHAR(100) COMMENT '微信ｉｄ',
  `from_user_name` VARCHAR(100) COMMENT '微信昵称',
  `from_nick_name` VARCHAR(100) COMMENT '微信昵称',
  `msg_type` VARCHAR(100) COMMENT '消息类型',
  `key_word` VARCHAR(100) COMMENT '关键字',
  `content` text COMMENT '内容',
  `send_time` datetime comment '发送时间',
  `created_time` datetime comment '创建时间',
  PRIMARY KEY (`id`)
)
COMMENT='群成长信息记录'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1000
;

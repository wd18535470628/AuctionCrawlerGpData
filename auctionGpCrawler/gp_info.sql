/*
SQLyog  v12.2.6 (64 bit)
MySQL - 5.7.20-log : Database - gp_info
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`gp_info` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `gp_info`;

/*Table structure for table `gp_auction_info` */

DROP TABLE IF EXISTS `gp_auction_info`;

CREATE TABLE `gp_auction_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` varchar(10) DEFAULT NULL COMMENT '标的物id',
  `court_id` varchar(10) DEFAULT NULL COMMENT '法院id',
  `title` varchar(60) DEFAULT NULL COMMENT '标的物名称',
  `kind_id` varchar(10) DEFAULT NULL COMMENT '标的物类型id',
  `url` varchar(80) DEFAULT NULL COMMENT 'url地址',
  `start_price` varchar(80) DEFAULT NULL COMMENT '起拍价',
  `current_price` varchar(80) DEFAULT NULL COMMENT '成交价(或当前价)',
  `cash_deposit` varchar(80) DEFAULT NULL COMMENT '保证金',
  `payment_advance` varchar(80) DEFAULT NULL COMMENT '变卖预缴款',
  `access_price` varchar(80) DEFAULT NULL COMMENT '评估价',
  `fare_increase` varchar(80) DEFAULT NULL COMMENT '加价幅度',
  `paimai_times` varchar(10) DEFAULT NULL COMMENT '拍卖次数',
  `paimai_type` varchar(20) DEFAULT NULL COMMENT '拍卖方式',
  `delay_cycle` varchar(80) DEFAULT NULL COMMENT '延时周期',
  `corporate_agent` varchar(30) DEFAULT NULL COMMENT '联系人',
  `phone` varchar(50) DEFAULT NULL COMMENT '电话',
  `selling_period` varchar(30) DEFAULT NULL COMMENT '变卖期',
  `online_cycle` varchar(10) DEFAULT NULL COMMENT '在线拍周期',
  `bidding_record` varchar(10) DEFAULT NULL COMMENT '竞价记录',
  `paimai_model` varchar(10) DEFAULT NULL COMMENT '拍卖模式',
  `enrollment` varchar(10) DEFAULT NULL COMMENT '报名人数',
  `set_reminders` varchar(10) DEFAULT NULL COMMENT '提醒人数',
  `onlookers` varchar(10) DEFAULT NULL COMMENT '围观人数',
  `data_time` varchar(50) DEFAULT NULL COMMENT '数据更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2281 DEFAULT CHARSET=utf8;

/*Table structure for table `gp_auction_kind` */

DROP TABLE IF EXISTS `gp_auction_kind`;

CREATE TABLE `gp_auction_kind` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `auction_type` varchar(10) DEFAULT NULL,
  `auction_desc` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Table structure for table `gp_auction_status` */

DROP TABLE IF EXISTS `gp_auction_status`;

CREATE TABLE `gp_auction_status` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `auction_status` varchar(10) DEFAULT NULL,
  `auction_desc` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Table structure for table `gp_court_info` */

DROP TABLE IF EXISTS `gp_court_info`;

CREATE TABLE `gp_court_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `court_id` varchar(60) DEFAULT NULL,
  `court_name` varchar(60) DEFAULT NULL,
  `city` varchar(60) DEFAULT NULL,
  `province` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3485 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

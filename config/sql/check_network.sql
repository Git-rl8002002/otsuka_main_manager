/*
* Author   : JasonHung
* Date     : 20220717
* Update   : 20230718
* Function : otsuka check invoice errors history
*/

/*
 * database otsuka_check_network
 */ 
create database otsuka_check_network DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_check_network;

/* 
 * check_record
 */
create table check_network(
no int not null primary key AUTO_INCREMENT,
c_date date null,
c_ip varchar(100) null,
c_isp varchar(100) null,
c_country varchar(100) null,
c_region_name varchar(100) null,
c_city varchar(100) null,
c_lon varchar(100) null,
c_lat varchar(100) null,
c_status varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


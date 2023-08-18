/*
* Author   : JasonHung
* Date     : 20220818
* Update   : 20230818
* Function : otsuka backup record from NAS
*/

/*
 * database otsuka_check_network
 */ 
create database otsuka_backup_nas DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_backup_nas;

/* 
 * check_record
 */
create table backup_record(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_time time null,
d_name varchar(100) null,
u_file varchar(100) null,
f_size varchar(50) null,
r_status varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


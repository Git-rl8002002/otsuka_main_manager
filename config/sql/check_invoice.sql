/*
* Author   : JasonHung
* Date     : 20220717
* Update   : 20230717
* Function : otsuka check invoice errors history
*/

/*
 * database otsuka_invoice_history
 */ 
create database otsuka_invoice_history DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_invoice_history;

/* 
 * check_record
 */
create table check_record(
no int not null primary key AUTO_INCREMENT,
c_date date null,
C5 varchar(30) null,
D5 varchar(30) null,
E5 varchar(30) null,
F5 varchar(30) null,
G5 varchar(30) null,
H5 varchar(30) null,
J5 varchar(30) null,
K5 varchar(30) null,
c_status varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* 
 * run_check_record
 */
create table run_check_record(
no int not null primary key AUTO_INCREMENT,
c_date datetime null,
r_date date null,
r_time time null,
c_status varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/*
* Author   : JasonHung
* Date     : 20220717
* Update   : 20230717
* Function : otsuka check card reader
*/

/*
 * database otsuka_invoice_history
 */ 
create database otsuka_company_server DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_company_server;

/* 
 * success_record
 */
create table server_record(
no int not null primary key AUTO_INCREMENT,
c_date datetime null,
r_date date null,
r_time time null,
r_server varchar(100) null,
r_ip varchar(100) null,
r_user varchar(50) null,
r_pwd varchar(50) null,
r_note text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




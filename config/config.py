#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230720
# Function : otsuka factory work time record

#############
#
# variable
#
#############
parm = {'title':'台灣大塚製藥'}

###################
#
# otsuka_factory
#
###################
otsuka_factory  = {'host':'192.168.1.93' , 'port':3306 , 'user':'otsuka'     , 'pwd':'OtsukatW168!'      , 'db':'otsuka_factory' , 'charset':'utf8'}
otsuka_factory2 = {'host':'192.168.1.35' , 'port':3306 , 'user':'HR2BPM'     , 'pwd':'Otsukatw14001297!' , 'db':'Agentflow'      , 'charset':'utf8'}
otsuka_factory3 = {'host':'192.168.1.31' , 'port':3306 , 'user':'Jason_Hung' , 'pwd':'e03vu,4timqotu!'   , 'db':'SHRM'           , 'charset':'utf8'}

#############
#
# txt path
#
#############
txt_path = {'linux_txt_path':'/var/www/html/medicine/txt/' , 'linux_pdf_path':'/var/www/html/medicine/pdf/nas/backup_record.txt'}


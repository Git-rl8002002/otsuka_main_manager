# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230714
# update   : 20230718
# Function : variables parameters

#####################################################################################
#
# MySQL
# 
#####################################################################################
dir_path = "C:/Jason_python/invoice_check/file"
db       = {'host':'192.168.1.93' , 'port':3306 , 'user' : 'otsuka', 'pwd':'OtsukatW168!' , 'db':'otsuka_invoice_history' , 'charset':'utf8'}
db2      = {'host':'192.168.1.93' , 'port':3306 , 'user' : 'otsuka', 'pwd':'OtsukatW168!' , 'db':'otsuka_check_network'   , 'charset':'utf8'}
db3      = {'host':'192.168.1.93' , 'port':3306 , 'user' : 'otsuka', 'pwd':'OtsukatW168!' , 'db':'otsuka_backup_nas'      , 'charset':'utf8'}

#####################################################################################
#
# line notify
#
#####################################################################################
# 1 by 1(jason)
token = 'G2caVYeO1TmbabvCu2j7sUMmaMLmrhlwt8YSW25tMWA'
            
# 1 by many(Otsuka IT)
token2 = 'sBXL6uZvu6qLoWQOXisF79Qd7XPhko91Ley5MCKyt2Q'


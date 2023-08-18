# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230714
# update   : 20230718
# Function : check invoice email attachments content errors

import requests , logging , time , pymysql , socket , sys
from variables import *

#####################################################################################
#
# class - check_network
#
#####################################################################################
class check_network:
    
    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self , search_ip):

        self.check_ip(search_ip)

    ###########
    # add_db
    ###########
    def add_db(self , ip , isp , country , region_name , city , lon , lat , status):
        
        conn = pymysql.connect(host=db2['host'],port=db2['port'],user=db2['user'],passwd=db2['pwd'],database=db2['db'],charset=db2['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            now_day = time.strftime("%Y-%m-%d" , time.localtime())

            check_sql = "select c_ip from check_network where c_ip='{0}'".format(ip)
            curr.execute(check_sql)
            check_res = curr.fetchone()

            if check_res is None:
                
                sql  = "insert into check_network(c_date , c_ip , c_isp , c_country , c_region_name , c_city , c_lon , c_lat , c_status) "
                sql += "value('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , '{6}' , '{7}' , '{8}')".format(now_day , ip , isp , country , region_name , city , lon , lat , status)
                
                curr.execute(sql)
                conn.commit()

            else:
                print('\n')
                print('----------------------------------------------------------------------------\n')
                logging.info("IP : {0} , 已經存在.".format(ip))

        except Exception as e:
            logging.info('< Error > update_db : ' + str(e))
        finally:
            conn.close()

    ##################
    # find_local_ip
    ##################
    def find_local_ip(self):
        try:
            hostname = socket.gethostname()
            ip_addr  = socket.gethostbyname(hostname)

            logging.info('本機 IP : ' + str(ip_addr))

        except Exception as e:
            logging.info('< Error > find_local_ip : ' + str(e))
        finally:
            pass

    #############
    # check_ip
    #############
    def check_ip(self , ip_address):
        try:
            url  = "http://ip-api.com/json/" + ip_address
            res  = requests.get(url)
            data = res.json()

            if data['status'] == 'fail':
                logging.info('IP : ' + str(ip_address) + ' , 查詢失敗 !')

            else:
                print('\n')
                print('----------------------------------------------------------------------------\n')
                logging.info('IP : '  + str(data['query']))
                logging.info('國家 : ' + str(data['country']))
                logging.info('國碼 : ' + str(data['countryCode']))
                logging.info('地區 : ' + str(data['regionName']))
                logging.info('ISP : '  + str(data['isp']))
                logging.info('城市 : ' + str(data['city']))
                logging.info('郵遞區號 : ' + str(data['zip']))
                logging.info('經度 : ' + str(data['lon']))
                logging.info('緯度 : ' + str(data['lat']))

                ############################
                # check ip and save to db
                ############################
                self.add_db(str(data['query']) , str(data['isp']) , str(data['country']) , str(data['regionName']) , str(data['city']) , str(data['lon']) , str(data['lat']) , str(data['status']))

        except Exception as e:
            logging.info('< Error > check_ip : ' + str(e))
        finally:
            pass

#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    ### usage
    if len(sys.argv) < 2:
        print("#############################################################################################################")
        print("#")
        print("# Example : ")
        print("# \t ( 用中華電信 IP 找出相關資訊 : 168.95.1.1 ) ./network_dao.py 168.95.1.1 ")
        print("#")
        print("#############################################################################################################")
    else:
        ##################
        # check network
        ##################
        check_network = check_network(sys.argv[1])
        
    
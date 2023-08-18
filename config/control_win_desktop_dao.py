# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230801
# update   : 20230802
# Function : check chatgpt v3.5

import requests , logging , time , pymysql , socket , sys , openai , csv , pyautogui , win32api
import asyncio , websockets , ctypes
from variables import *
from pywinauto import Application

#####################################################################################
#
# class - check_chatgpt
#
#####################################################################################
class check_chatgpt:
    
    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self):
        pass

    ########################
    # control_win_desktop
    ########################
    def control_win_desktop(self):
        try:
            pass
        except Exception as e:
            logging.info('< Error > control_win_desktop : ' + str(e))
        finally:
            pass

    #######################
    # db_record_save_csv
    #######################
    def db_record_save_csv(self):
        
        conn = pymysql.connect(host=db2['host'],port=db2['port'],user=db2['user'],passwd=db2['pwd'],database=db2['db'],charset=db2['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            now_day = time.strftime("%Y-%m-%d" , time.localtime())

            check_sql = "select c_date , c_ip , c_isp , c_country , c_region_name , c_city from check_network"
            curr.execute(check_sql)
            check_res = curr.fetchall()

            ##################
            # save to csv 1
            ##################
            file_path = 'F:/otsuka/Git/check_otsuka_data/file/' + now_day + '_1.csv'

            with open(file_path , mode='w' , newline='') as file:
                write = csv.writer(file)
                write.writerow(['Date','IP','ISP','Country','region_name','City'])
                write.writerows(check_res) 

            logging.info('csv1 , save to csv file successful.')

            ##################
            # save to csv 2
            ##################
            file_path2 = 'F:/otsuka/Git/check_otsuka_data/file/' + now_day + '_2.csv'
            
            with open(file_path2 , mode='a' , newline='') as csv2:
                writer = csv.writer(csv2)
                writer.writerow(['Date','IP','ISP','Country','region_name','City'])
                writer.writerows(check_res)

            logging.info('csv2 , save to csv file successful.')

        except Exception as e:
            logging.info('< Error > db_record_save_csv : ' + str(e))

        finally:
            conn.close()

    ##############
    # db_record
    ##############
    def db_record(self , ip , isp , country , region_name , city , lon , lat , status):
        
        conn = pymysql.connect(host=db2['host'],port=db2['port'],user=db2['user'],passwd=db2['pwd'],database=db2['db'],charset=db2['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            now_day = time.strftime("%Y-%m-%d" , time.localtime())

            check_sql = "select c_ip , c_isp , c_country , c_region_name , c_city from check_network where c_ip='{0}'".format(ip)
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
            logging.info('< Error > db_record : ' + str(e))
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

    ##################
    # check_chatgpt
    #################
    def check_chatgpt(self , prompt , max_tokens=500):
        try:
            response = openai.Completion.create(
                #engine="text-davinci-002",
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()   

        except Exception as e:
            logging.info('< Error > check_chatgpt : ' + str(e))
        finally:
            pass
    
    ###########################
    # check_chatgpt_requests
    ###########################
    def check_chatgpt_requests(self , api_key):
        try:
            response = requests.post(
                'https://api.openai.com/v1/completions',
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json = {
                    'model': 'text-davinci-003',
                    'prompt': 'hello , I am jason who are you ?',
                    'temperature': 0.4,
                    'max_tokens': 30
                }
            )
            res = response.json()
            print(res['choices'][0]['text'])

            ################
            # save to csv
            ################
            data = [
                        ['Name', 'Age', 'City'],
                        ['John', 30, 'New York'],
                        ['Jane', 25, 'Los Angeles'],
                        ['Mike', 35, 'Chicago']
                    ]
            
            

            print("save to output.csv ok")
            
        except Exception as e:
            logging.info('< Error > check_chatgpt_requests : ' + str(e))
        finally:
            pass

#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
 
    api_key = "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"
    openai.api_key = api_key

    res_chat = check_chatgpt()

    ###########################
    # check_chatgpt_requests
    ###########################
    #res_chat.check_chatgpt_requests(api_key)
    res_chat.control_win_desktop()
    #res_chat.control_windows()
    

    ##################
    # check chatgpt
    ##################
    '''
    print("ChatGPT : hello ! I'am ChatGPT May I Help you ?")

    while True:
        user_input = input("You: ")
 
        if user_input.lower() in ['exit','quit','bye']:
            print("ChatGPT , goodbye !")
            break
        
        response = res_chat.check_chatgpt(user_input)
        print("ChatGPT : " + str(response))
    '''

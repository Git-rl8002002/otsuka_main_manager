# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230801
# update   : 20230802
# Function : check chatgpt v3.5

import requests , logging , time , pymysql , socket , sys , openai , csv , psutil , speedtest , os
from variables import *
from pysnmp.hlapi import *
import paramiko , pysftp as sftp , shutil


import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

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
    
    ##################
    # learn_mechine
    ##################
    def learn_mechine(self):
        try:
            # 加载鸢尾花数据集
            data = load_iris()
            X = data.data
            y = data.target

            # 将数据划分为训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 特征缩放
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # 创建逻辑回归模型并进行训练
            model = LogisticRegression()
            model.fit(X_train_scaled, y_train)

            # 预测测试集
            y_pred = model.predict(X_test_scaled)

            # 计算准确率
            accuracy = accuracy_score(y_test, y_pred)
            print("Accuracy:", accuracy)

        except Exception as e:
            logging.info('< Error > learn mechine : ' + str(e))
        finally:
            pass
    
    #######
    # pd
    #######
    def pd(self):
        try:
            data = {'name' : ['hung','jason','redman','rl8002002'],
                    'age' : [22,25,30,35]}
            df = pd.DataFrame(data)

            head = df.head()
            sum = df.describe()
            ages = df['age']


            young_people = df[df['age'] < 25]
            mid_people = df[df['age'] < 30]
            old_people = df[df['age'] < 35]
            
            name = df[df['name'] == 'jason']

            print(f"name = {name}")
            
        except Exception as e:
            logging.info('< Error > pd : ' + str(e))
        finally:
            pass
    
    #####################
    # pc_usaged_status
    #####################
    def pc_usaged_status(self):
        try:
            

            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            hdd_usage = psutil.disk_usage('/').percent
            network_io = psutil.net_io_counters()

            print(f"cpu usage : {cpu_usage} %")
            print(f"ram usage : {ram_usage} %")
            print(f"hdd usage : {hdd_usage} %")
            print(f"network IO : {network_io}")
            print(f"name : {psutil.users()}")

        except Exception as e:
            logging.info('< Error > pc_usaged_status :' + str(e))
        finally:
            pass    
       
    ###############
    # test_speed
    ###############
    def test_speed(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            download_speed = st.download() / 1024 / 1024
            upload_speed = st.upload() / 1024 / 1024

            print(f"Download speed : {download_speed:.2f} Mbps")
            print(f"Upload speed : {upload_speed:.2f} Mps")

            
        except Exception as e:
            logging.info('< Error > pc_usaged_status :' + str(e))
        finally:
            pass 
    
    
    
    
    
    ####################
    # backup_qsan_nas
    ####################
    def backup_qsan_nas(self , host, port, user, pwd, dir_name , upload_file):
        
        try:
            # time record
            now_day = time.strftime("%Y-%m-%d" , time.localtime())
            
            cnopts = sftp.CnOpts()
            cnopts.hostkeys = None
            
            print('\n----------------------------------------------------------------------------------------------')

            #########
            # Sftp
            #########
            psftp = sftp.Connection(host=host , username=user , password=pwd , port=port , cnopts=cnopts)
            
            #############################################
            # layer 1 - go to QSAN NAS backup document  
            #############################################
            psftp.chdir('/backup')
            try:
                ###########################
                # layer 2 - by every day 
                ###########################
                try: 
                    psftp.chdir(now_day)
                    ########################
                    # layer 3 - by server  
                    ########################
                    try:
                        psftp.chdir(dir_name)
                        logging.info(f'{dir_name} - upload starting...')
                        try:
                            psftp.remove(upload_file)
                            psftp.put(upload_file)
                            logging.info(f'{dir_name} - upload finish.')

                        except FileNotFoundError:
                            psftp.put(upload_file)
                            logging.info(f'{dir_name} - upload finish.')

                    except FileNotFoundError:
                        logging.info(f'{dir_name} - upload starting...') 
                        psftp.mkdir(dir_name)
                        psftp.chdir(dir_name)
                        psftp.put(upload_file)
                        logging.info(f'{dir_name} - upload finish.')
                
                except FileNotFoundError:
                    logging.info(f'{dir_name} - upload starting...')
                    psftp.mkdir(now_day)
                    psftp.chdir(now_day)
                    psftp.mkdir(dir_name)
                    psftp.chdir(dir_name)
                    psftp.put(upload_file)
                    logging.info(f'{dir_name} - upload finish.')
            
            except FileNotFoundError:
                psftp.mkdir(now_day)
            
            psftp.close()

            print('----------------------------------------------------------------------------------------------')

        except Exception as e:
            logging.info('< Error > backup_qsan_nas :' + str(e))

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
    #res_chat.db_record_save_csv()


    ####################
    # upload QSAN NAS
    ####################
    while True:
        host = '192.168.1.55'
        port = 22
        user = 'admin'
        pwd  = 'ej/ck4vupvu3!'    

        dir_1 = 'dir_1'
        dir_2 = 'dir_2'
        dir_3 = 'dir_3'
        dir_4 = 'dir_4'
        dir_5 = 'dir_5'
        dir_6 = 'dir_6'
        dir_7 = 'dir_7'
        dir_8 = 'dir_8'
        dir_9 = 'dir_9'
        dir_10 = 'dir_10'

        upload    = {'upload_file1':'20230817.mp4','upload_file2':'20230428-PGM.mp4'}
        
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_1 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_2 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_3 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_4 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_5 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_6 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_7 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_8 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_9 , upload['upload_file1'])
        res_chat.backup_qsan_nas(host , port , user , pwd , dir_10 , upload['upload_file1'])
        
        time.sleep(60)
        
        

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

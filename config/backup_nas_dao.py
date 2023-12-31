# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230818
# update   : 20230828
# Function : otsuka backup db to nas 

import requests , logging , time , pymysql , socket , sys , openai , csv , psutil , speedtest , os
from variables import *
from pysnmp.hlapi import *
import paramiko , pysftp as sftp , shutil , socket , pyodbc , zipfile

import numpy as np
import pandas as pd

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

    #########################
    # backup_db_BPM_formal
    #########################
    def backup_db_BPM_formal(self):
        try:
            # time record
            now_day     = time.strftime("%Y%m%d" , time.localtime())
            now_time    = time.strftime("%H:%M:%S" , time.localtime())
            
            print('\n----------------------------------------------------------------------------------------------')
            
            ####################
            #　DB : Agentflow
            ####################
            host = '192.168.1.35'
            db   = 'Agentflow'
            db2  = 'Docpedia'
            user = 'HR2BPM'
            pwd  = 'Otsukatw14001297!'
            conn_str = f"DRIVER={{SQL Server}};SERVER={host};DATABASE={db};UID={user};PWD={pwd}"
            
            connection = pyodbc.connect(conn_str)
            connection.autocommit = True
            curr = connection.cursor()
            
            sql = f"BACKUP DATABASE [{db}] TO DISK = 'D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{db}_{now_day}.bak'"
            curr.execute(sql)
            curr.commit()
            logging.info(f'{db}_{now_day}.bak , database backup finish.')
            
            curr.close()
            connection.close()
            
            print('\n----------------------------------------------------------------------------------------------')
            
            ####################
            #　DB : Docpedia
            ####################
            host = '192.168.1.35'
            db   = 'Agentflow'
            db2  = 'Docpedia'
            user = 'HR2BPM'
            pwd  = 'Otsukatw14001297!'
            conn_str = f"DRIVER={{SQL Server}};SERVER={host};DATABASE={db2};UID={user};PWD={pwd}"
            
            connection = pyodbc.connect(conn_str)
            connection.autocommit = True
            curr = connection.cursor()
            
            sql2 = f"BACKUP DATABASE [{db2}] TO DISK = 'D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{db2}_{now_day}.bak'"
            curr.execute(sql2)
            curr.commit()
            logging.info(f'{db2}_{now_day}.bak , database backup finish.')
            
            curr.close()
            connection.close()
            
            print('\n----------------------------------------------------------------------------------------------')
            
            ####################
            #　attach file
            ####################
            zip_attach_file = 'attach_file_' + now_day + '.zip'
            
            with zipfile.ZipFile(zip_attach_file , 'w') as zip_file:
                zip_file.write('C:\\AttachFile' , arcname='AttachFile')
                logging.info('<msg> zip attach file successful.')

            print('\n----------------------------------------------------------------------------------------------')

        except Exception as e:
            logging.info('< Error > backup_db_BPM_formal : ' + str(e))
        finally:
            pass


    #######################
    # backup_db_BPM_test
    #######################
    def backup_db_BPM_test(self):
        try:
            # time record
            now_day     = time.strftime("%Y%m%d" , time.localtime())
            now_time    = time.strftime("%H:%M:%S" , time.localtime())

            host = '192.168.1.37'
            db1  = 'Agentflow'
            db2  = 'Docpedia'
            user = 'HR2BPM'
            pwd  = 'Otsukatw14001297!'
            conn_str = f"DRIVER={{SQL Server}};SERVER={host};DATABASE={db1};UID={user};PWD={pwd}"
            
            connection = pyodbc.connect(conn_str)
            connection.autocommit = True
            curr = connection.cursor()

            ####################
            #　DB : Agentflow
            ####################
            sql1 = f"BACKUP DATABASE [{db1}] TO DISK = 'D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{db1}_{now_day}.bak'"
            curr.execute(sql1)
            curr.commit()
            print(f'{db1}_{now_day}.bak , database backup finish.')
            
            curr.close()
            connection.close()

            ####################
            #　DB : Docpedia
            ####################
            host = '192.168.1.37'
            db1  = 'Agentflow'
            db2  = 'Docpedia'
            user = 'HR2BPM'
            pwd  = 'Otsukatw14001297!'
            conn_str = f"DRIVER={{SQL Server}};SERVER={host};DATABASE={db2};UID={user};PWD={pwd}"
            
            connection = pyodbc.connect(conn_str)
            connection.autocommit = True
            curr = connection.cursor()
            
            sql2 = f"BACKUP DATABASE [{db2}] TO DISK = 'D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{db2}_{now_day}.bak'"
            curr.execute(sql2)
            curr.commit()
            print(f'{db2}_{now_day}.bak , database backup finish.')
            
            curr.close()
            connection.close()

        except Exception as e:
            logging.info('< Error > backup_db_BPM_test : ' + str(e))
        finally:
            pass
    

    #########################
    # backup_nas_db_record
    #########################
    def backup_nas_db_record(self , dir_name , upload_file , f_size , r_status):
        
        conn = pymysql.connect(host=db3['host'],port=db3['port'],user=db3['user'],passwd=db3['pwd'],database=db3['db'],charset=db3['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            now_day  = time.strftime("%Y-%m" , time.localtime())
            now_day2 = time.strftime("%Y-%m-%d" , time.localtime())
            now_time = time.strftime("%H:%M:%S" , time.localtime())

            sql  = "create table `{0}`(no int not null primary key AUTO_INCREMENT,r_date date null,r_time time null,d_name varchar(100) null,u_file varchar(100) null,f_size varchar(50) null,r_host varchar(50) null,r_ip varchar(50) null,r_status varchar(50) null)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci".format(now_day)
            curr.execute(sql)
            conn.commit()
            
            logging.info(f'create tb : {now_day2} successful.')

        except Exception as e:
            f_size    = str(f_size) + str(' MB')
            host_name = socket.gethostname()
            host_ip   = socket.gethostbyname(host_name)

            sql  = "insert into `{5}`(r_date , r_time , d_name , u_file , r_status , f_size , r_host , r_ip) value('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{6}' , '{7}' , '{8}')".format(now_day2 , now_time , dir_name , upload_file , r_status , now_day , f_size , host_name , host_ip)
            curr.execute(sql)
            conn.commit()

            logging.info(f'add data to tb : {now_day2} successful.')

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
    # backup_qsan_nas2
    ####################
    def backup_qsan_nas2(self , host, port, user, pwd, dir_name , upload_file):
        
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
                        logging.info(f'{dir_name}/{upload_file} - upload starting...')
                        try:
                            psftp.remove(upload_file)
                            psftp.put(upload_file)
                            logging.info(f'{dir_name}/{upload_file} - upload finish.')
                            
                            ### backup nas record mysql
                            f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                            self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')

                        except FileNotFoundError:
                            psftp.put(upload_file)
                            logging.info(f'{dir_name}/{upload_file} - upload finish.')
                            
                            ### backup nas record mysql
                            f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                            self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')

                    except FileNotFoundError:
                        logging.info(f'{dir_name}/{upload_file} - upload starting...') 
                        psftp.mkdir(dir_name)
                        psftp.chdir(dir_name)
                        psftp.put(upload_file)
                        logging.info(f'{dir_name}/{upload_file} - upload finish.')
                        
                        ### backup nas record mysql
                        f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                        self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')
                
                except FileNotFoundError:
                    logging.info(f'{dir_name}/{upload_file} - upload starting...')
                    psftp.mkdir(now_day)
                    psftp.chdir(now_day)
                    psftp.mkdir(dir_name)
                    psftp.chdir(dir_name)
                    psftp.put(upload_file)
                    logging.info(f'{dir_name}/{upload_file} - upload finish.')
                    
                    ### backup nas record mysql
                    f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                    self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')
            
            except FileNotFoundError:
                psftp.mkdir(now_day)
            
            psftp.close()

            print('----------------------------------------------------------------------------------------------')

        except Exception as e:
            logging.info('< Error > backup_qsan_nas :' + str(e))

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
            psftp.chdir('/backup_temp')
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
                        logging.info(f'{dir_name}/{upload_file} - upload starting...')
                        try:
                            psftp.remove(upload_file)
                            psftp.put(upload_file)
                            logging.info(f'{dir_name}/{upload_file} - upload finish.')
                            
                            ### backup nas record mysql
                            f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                            self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')

                        except FileNotFoundError:
                            psftp.put(upload_file)
                            logging.info(f'{dir_name}/{upload_file} - upload finish.')
                            
                            ### backup nas record mysql
                            f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                            self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')

                    except FileNotFoundError:
                        logging.info(f'{dir_name}/{upload_file} - upload starting...') 
                        psftp.mkdir(dir_name)
                        psftp.chdir(dir_name)
                        psftp.put(upload_file)
                        logging.info(f'{dir_name}/{upload_file} - upload finish.')
                        
                        ### backup nas record mysql
                        f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                        self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')
                
                except FileNotFoundError:
                    logging.info(f'{dir_name}/{upload_file} - upload starting...')
                    psftp.mkdir(now_day)
                    psftp.chdir(now_day)
                    psftp.mkdir(dir_name)
                    psftp.chdir(dir_name)
                    psftp.put(upload_file)
                    logging.info(f'{dir_name}/{upload_file} - upload finish.')
                    
                    ### backup nas record mysql
                    f_size = round((psftp.stat(upload_file).st_size)/1024/1024 , 2)
                    self.backup_nas_db_record(dir_name , upload_file , f_size , 'ok')
            
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
 
    ####################
    #
    # chatgpt api key
    #
    ####################
    api_key = "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"
    openai.api_key = api_key
    
    res_chat = check_chatgpt()
    
    ##############################################################
    #
    # backup MSSQL backup MSSQL database : Agentflow , Docpedia
    #
    ##############################################################
    res_chat.backup_db_BPM_formal()
    

    ###########################################################################
    #
    # backup MSSQL backup MSSQL database : Agentflow , Docpedia , AttachFile
    #
    ###########################################################################
    now_day = time.strftime("%Y%m%d" , time.localtime())
    b_file1 = 'Agentflow_' + now_day + '.bak'
    b_file2 = 'Docpedia_' + now_day + '.bak'

    file_1_path = f"D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{b_file1}"
    file_2_path = f"D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\{b_file2}"
    
    while True:
        ##################################
        #
        # check .bak backup file exists
        #
        ##################################
        if os.path.exists(file_1_path) and os.path.exists(file_2_path):
           
           ####################
            #
            # upload QSAN NAS
            #
            ####################
            while True:
                
                # now day
                now_day = time.strftime("%Y%m%d" , time.localtime())

                host = '192.168.1.55'
                port = 22
                user = 'admin'
                pwd  = 'ej/ck4vupvu3!'    

                dir = {'d_1':'BPM_test' , 'd_2':'BPM_formal'}
                b_file1 = 'Agentflow_'  + now_day + '.bak'
                b_file2 = 'Docpedia_'   + now_day + '.bak'
                b_file3 = 'AttachFile_' + now_day + '.zip'
                
                ####################################
                #
                # Agentflow .bak send to QSAN NAS
                #
                ####################################
                res_chat.backup_qsan_nas(host , port , user , pwd , dir['d_2'] , b_file1)
                #shutil.move(file_1_path , backup_1_path)
                
                ###################################
                #
                # Docpedia .bak send to QSAN NAS
                #
                ###################################
                res_chat.backup_qsan_nas(host , port , user , pwd , dir['d_2'] , b_file2)
                #shutil.move(file_2_path , backup_2_path)
                
                ######################################
                #
                # attach file .zip send to QSAN NAS
                #
                ######################################
                output_path = 'D:\\MSSQL\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup\\otsuka_main_manager\\AttachFile_' + now_day
                folder_path = 'C:\\AttachFile'
                
                shutil.make_archive(output_path, 'zip', folder_path)
                res_chat.backup_qsan_nas(host , port , user , pwd , dir['d_2'] , b_file3)

                print('\n----------------------------------------------------------------------------------------------')
                
                ###################################################################################
                #
                # 每天晚上 11:50 Agentflow.bak , Docpedia.bak , AttachFile.zip 丟到 backup (write once) document
                #
                ###################################################################################
                write_once_time = time.strftime("%Y-%m-%d %H:%M" , time.localtime())
                check_time      = now_day + ' 23:50'
                
                if write_once_time == check_time:
                    
                    # Agentflow .bak
                    res_chat.backup_qsan_nas2(host , port , user , pwd , dir['d_2'] , b_file1)
                    
                    # Docpedia .bak
                    res_chat.backup_qsan_nas2(host , port , user , pwd , dir['d_2'] , b_file2)
                    
                    # AttachFile .zip
                    res_chat.backup_qsan_nas(host , port , user , pwd , dir['d_2'] , b_file3)
                    
                else:
                    logging.info('< Msg > backup to write once not this time.')
                
                time.sleep(900)  
        else:
            logging.info(f"{b_file1} , {b_file2} , 文件不存在。")
            time.sleep(60)
    
    

    

    
        

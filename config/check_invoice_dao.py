# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230714
# update   : 20230714
# Function : check invoice email attachments errors

import requests , logging , time , win32com.client , os , zipfile , xlrd , pymysql , socket
from variables import *

#####################################################################################
#
# class - invoice_check
#
#####################################################################################
class invoice_check:
    
    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")
   
    #########
    # init
    #########
    def __init__(self):
        try:

            while True: 
                self.check_invoice_email()
                time.sleep(3600)
            
        except Exception as e:
            logging.info('< Error > init : ' + str(e))
        finally:
            pass

    ################
    # check_excel
    ################
    def check_excel(self , excel_file):
        try:
            # now_date
            now_day = time.strftime("%Y-%m-%d" , time.localtime()) 

            # save attachments path 
            data_dir = dir_path

            
            data = excel_file.split('.')
            excel_file = data[0] + '.xls'

            #################
            #　check excel
            #################
            wb = xlrd.open_workbook(data_dir + '/' + excel_file)
            
            ### 顯示全部分頁 sheet
            #sheet = wb.sheet_names()
            #print(sheet)
            
            ###  顯示第一張分頁
            sheet1 = wb.sheet_by_index(0)
            
            C5_val = sheet1.cell(4,2).value  # 1-1 傳輸成功
            D5_val = sheet1.cell(4,3).value  # 1-2 傳輸異常
            E5_val = sheet1.cell(4,4).value  # 2-1 回覆成功
            F5_val = sheet1.cell(4,5).value  # 2-2 回覆異常
            G5_val = sheet1.cell(4,6).value  # 3-1 存證成功
            H5_val = sheet1.cell(4,7).value  # 3-3 存證異常
            J5_val = sheet1.cell(4,9).value  # (1-1)-(2-1) 傳輸差異數
            K5_val = sheet1.cell(4,10).value # (2-1)-(3-1) 存證差異數

            #######################
            # check MySQL record
            #######################
            conn = pymysql.connect(host=db['host'],port=db['port'],user=db['user'],passwd=db['pwd'],database=db['db'],charset=db['charset'])    
            curr = conn.cursor()

            try:
                check_sql = "select c_date from check_record where c_date='{0}'".format(now_day)
                curr.execute(check_sql)
                res = curr.fetchone()
            
                if res is None:
                    sql = "insert into check_record(c_date , C5 , D5 , E5 , F5 , G5 , H5 , J5 , K5) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(now_day , int(C5_val) , int(D5_val) , int(E5_val) , int(F5_val) , int(G5_val) , int(H5_val) , int(J5_val) , int(K5_val))
                    curr.execute(sql)

                    conn.commit()

                    ################
                    # line notify
                    ################
                    self.line_notify(C5_val , D5_val , E5_val , F5_val , G5_val , H5_val , J5_val , K5_val , token2)

                    print('\n')
                    print('---------------------------------------------------------------')
                    logging.info(now_day + ' 檢查歷史存證檢核表內容完成後 line 推撥告知完成.')

                else:
                    print('\n')
                    print('---------------------------------------------------------------')
                    logging.info(str('日期 : ') + now_day + str(' , 比對檢查電子發票存證檢核紀錄 , 已完成.'))

                    #####################################
                    # run check invoice history record
                    #####################################
                    self.run_check_record()

            except Exception as e:
                logging.info('< Error > connect MySQL : ' + str(e))
                
            finally:
                conn.close()

        except Exception as e:
            logging.info('< Error > check_excel : ' + str(e))
        finally:
            pass

    ###############
    # unzip_file
    ###############
    def unzip_file(self):
        try:
            # now_date
            now_day = time.strftime("%Y%m%d" , time.localtime()) 

            # save attachments path 
            #data_dir = "C:/Jason_python/invoice_check/file"
            data_dir = dir_path
            
            for folder , sub_folder , file_name in os.walk(data_dir):
                for sub_file_name in file_name:
                    
                    # check now day and sub file name is .zip than unzip
                    today_file = sub_file_name.split('.')
                    
                    if sub_file_name.find(now_day) == 0 and today_file[1] == 'zip':
                        with zipfile.ZipFile(data_dir + '/' + sub_file_name , 'r') as zf:
                            zf.extractall(path=data_dir)

                            print('\n')
                            print('---------------------------------------------------------------')
                            logging.info(sub_file_name + ' 歷史存證檢核表 , 解壓縮完成.')

                            self.check_excel(sub_file_name)
                    
                        
        except Exception as e:
            logging.info('< Error > unzip_file : ' + str(e))
        finally:
            pass

    ########################
    # check_invoice_email
    ########################
    def check_invoice_email(self):
        try:
            # now_date
            now_day = time.strftime("%Y%m%d" , time.localtime()) 
            
            # save attachments path 
            #data_dir = "C:/Jason_python/invoice_check/file"
            data_dir = dir_path


            outlook     = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox       = outlook.GetDefaultFolder(6)  # 6代表收件箱，默认值为6
            messages    = inbox.Items
            
            print("\n")
            print('---------------------------------------------------------------')
            logging.info('收取 ' + now_day + ' , 歷史存證檢核表 \n')

            for message in messages:
                if message.Subject.find('歷史存證檢核表') == 26:
                    print("信主题 : "  +  message.Subject)
                    print("寄信人 : " + message.SenderName)

                    attachments = message.Attachments
                    for attachments in attachments:
                        file_name = attachments.Filename
                        print("附件檔 : " + file_name)
    
                        ### 0 = 相同檔名 , -1 = 不同檔名
                        if file_name.find(now_day) == 0: 
                            save_path = os.path.join(data_dir , file_name)
                            attachments.SaveAsFile(save_path)

                            print("存附件 : " + file_name)
                            
                            print("\n")

            self.unzip_file()
                            
        except Exception as e:
            logging.info('< Error > check_invoice_email : ' + str(e))
        finally:
            pass

    ########################
    # success_record_file
    ########################
    def success_record_file(self,record_txt):
        try:
            ### time record
            now_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 
            
            file = open("success_record.txt" , "a")    
            r_txt = now_time + " " + record_txt
            file.write(r_txt)
            file.close()

        except Exception as e :
            logging.info('< Error > success_record_file :' + str(e))
        finally:
            pass

    #####################
    # fail_record_file
    #####################
    def fail_record_file(self,record_txt):
        try:
            # time record
            now_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 
            
            file = open("fail_record.txt" , "a")    
            r_txt = now_time + " " + record_txt
            file.write(r_txt)
            file.close()

        except Exception as e :
            logging.info('< Error > fail_record_file : ' + str(e))
        finally:
            pass


    #####################
    # run_check_record
    #####################
    def run_check_record(self):
        
        conn = pymysql.connect(host=db['host'],port=db['port'],user=db['user'],passwd=db['pwd'],database=db['db'],charset=db['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            r_day   = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_date  = time.strftime("%Y-%m-%d" , time.localtime())
            r_time  = time.strftime("%H:%M:%S" , time.localtime())

            sql = "insert into run_check_record(c_date , r_date , r_time , c_status) value('{0}' , '{1}'  , '{2}' , '{3}')".format(r_day , r_date , r_time , 'runned')
            curr.execute(sql)
            conn.commit()

        except Exception as e:
            logging.info('< Error > run_check_record : ' + str(e))
        finally:
            conn.close()

    #########################
    # update_upload_record
    #########################
    def update_upload_record(self , c_status):
        
        conn = pymysql.connect(host=db['host'],port=db['port'],user=db['user'],passwd=db['pwd'],database=db['db'],charset=db['charset'])    
        curr = conn.cursor()
        
        try:
            # time record
            now_day  = time.strftime("%Y-%m-%d" , time.localtime())

            sql = "update check_record set c_status='{0}' where c_date='{1}'".format(str(c_status),str(now_day))
            curr.execute(sql)
            conn.commit()

        except Exception as e:
            logging.info('< Error > update_upload_record : ' + str(e))
        finally:
            conn.close()

    ################
    # line_notify
    ################
    def line_notify(self,C5,D5,E5,F5,G5,H5,J5,K5 , token):
        
        try:
            # time record
            now_time  = time.strftime("%Y-%m-%d" , time.localtime())

            C5 = C5  # 1-1 傳輸成功
            D5 = D5  # 1-2 傳輸異常
            E5 = E5  # 2-1 回覆成功
            F5 = F5  # 2-2 回覆異常
            G5 = G5  # 3-1 存證成功
            H5 = H5  # 3-3 存證異常
            J5 = J5  # (1-1)-(2-1) 傳輸差異數
            K5 = K5  # (2-1)-(3-1) 存證差異數

            ################
            # 資料上傳正常
            ################
            if int(C5) == 0 and int(D5) == 0 and int(E5) == 0 and int(F5) == 0 and int(G5) == 0 and int(H5) == 0 and int(J5) == 0 and int(K5) == 0:  
                msg = '\n\n'
                msg += now_time + '  \n'
                msg += '電子發票歷史存證檢核表 \n\n' 
                msg += '傳輸成功 : ' + str(int(C5)) + '\t 傳輸異常 : ' + str(int(D5)) + '\n'
                msg += '回覆成功 : ' + str(int(E5)) + '\t 回覆異常 : ' + str(int(F5)) + '\n' 
                msg += '存證成功 : ' + str(int(G5)) + '\t 存證異常 : ' + str(int(H5)) + '\n' 
                msg += '傳輸差異數 : ' + str(int(J5)) + '\t 存證差異數 : ' + str(int(K5)) + '\n'
                msg += '\n\t<< 資料上傳正常 >>'

                headers = {
                "Authorization" : "Bearer " + token , 
                "Content-Type" : "application/x-www-form-urlencoded"
                }

                payload = {'message' : msg}
                r = requests.post("https://notify-api.line.me/api/notify" , headers=headers , data=payload) 
            
                ########################
                # success record file
                ########################
                if r.status_code == 200:
                    msg += '\n------------------------------------------------'
                    self.success_record_file(msg+"\n")

                    ###################################
                    # update upload record no errors
                    ###################################
                    self.update_upload_record('no error')

            else:
                ################
                # 資料上傳異常
                ################
                msg = '\n\n'
                msg += now_time + '  \n'
                msg += '電子發票歷史存證檢核表 \n\n' 
                msg += '傳輸成功 : ' + str(int(C5)) + '\t 傳輸異常 : ' + str(int(D5)) + '\n'
                msg += '回覆成功 : ' + str(int(E5)) + '\t 回覆異常 : ' + str(int(F5)) + '\n' 
                msg += '存證成功 : ' + str(int(G5)) + '\t 存證異常 : ' + str(int(H5)) + '\n' 
                msg += '傳輸差異數 : ' + str(int(J5)) + '\t 存證差異數 : ' + str(int(K5)) + '\n'
                msg += '\n\t<< 資料上傳異常 >>'
            
                headers = {
                    "Authorization" : "Bearer " + token , 
                    "Content-Type" : "application/x-www-form-urlencoded"
                }

                payload = {'message' : msg}
                r = requests.post("https://notify-api.line.me/api/notify" , headers=headers , data=payload) 
                
                #####################
                # fail record file
                #####################
                if r.status_code == 200:
                    msg += '\n------------------------------------------------'
                    self.fail_record_file(msg+"\n")

                    ################################
                    # update upload record errors
                    ################################
                    self.update_upload_record('error')
        
        except Exception as e:
            logging.info('< Error > line_notify : ' + str(e))
        finally:
            pass


#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    ##################
    # check network
    ##################
    check_invoice = invoice_check()
        
    
   
        
    
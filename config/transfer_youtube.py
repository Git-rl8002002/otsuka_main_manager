# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230714
# update   : 20230718
# Function : check invoice email attachments content errors

import requests , logging , time , pymysql , socket , sys
from variables import *
from pytube import YouTube

#####################################################################################
#
# class - transfer_youtube
#
#####################################################################################
class transfer_youtube:
    
    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self , url):

        self.transfer_youtube_mp4(url)

    #########################
    # transfer_youtube_mp4
    #########################
    def transfer_youtube_mp4(self , url , save_path='F:/download/mp4'):
        
        try:
            youtube = YouTube(url)

            d_video = youtube.streams.filter(progressive=True , file_extension='mp4').first()
            
            if d_video:
                print("Downloading : " + str(youtube.title))
                d_video.download(output_path=save_path)
                print("Download completed.")
            
            else:
                print("Video stream not available.")

        except Exception as e:
            logging.info('< Error > transfer_youtube : ' + str(e))
        
        finally:
            pass

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
        print("# \t ( use youtube url download :  ) ./transfer_youtube.py ")
        print("#")
        print("#############################################################################################################")
    else:
        #####################
        # download_youtube
        #####################
        download_youtube = transfer_youtube("https://www.youtube.com/watch?v=cEJtLjlpFeU")
        
    
# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230714
# update   : 20230721
# Function : check invoice email attachments content errors

import requests , logging , time , pymysql , socket , sys
from variables import *
from pysnmp.hlapi import *

#####################################################################################
#
# class - check_by_snmp
#
#####################################################################################
class check_by_snmp:

    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self , snmpwalk_ip):
        self.l7_by_snmp(snmpwalk_ip)
    
    ###############
    # l7_by_snmp
    ###############
    def l7_by_snmp(self , snmpwalk_ip):
        try:
            snmp_ip = snmpwalk_ip
            snmp_get_community = 'public'
            snmp_set_community = 'public'

            # 定義 MIB 根節點
            mib_root = ObjectIdentity('SNMPv2-MIB')

            # 創建 SNMP Walk 的 Generator
            snmp_walk_gen = bulkCmd(SnmpEngine(),
                                    CommunityData(snmp_get_community),
                                    UdpTransportTarget((snmp_ip, 161) , timeout=5),
                                    ContextData(),
                                    0, 25,  # NonRepeaters, MaxRepetitions
                                    ObjectType(mib_root))

            # 遞歸地遍歷並獲取所有數據
            for (errorIndication, errorStatus, errorIndex, varBinds) in snmp_walk_gen:
                if errorIndication:
                    logging.info('< Error> : ' + str(errorIndication))
                    break
                elif errorStatus:
                    logging.info('< Error > ' + str(errorStatus) + ' Index : ' + str(errorIndex))
                    break
                else:
                    for varBind in varBinds:
                        logging.info(varBind[0] + ' :　' + varBind[1])

        except Exception as e:
            logging.info('< Error > l7_by_snmp : ' + str(e))
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
        print("# \t ( 用 snmpwalk 跑一遍 ) ./check_l7_network.py 192.168.1.34 ")
        print("#")
        print("#############################################################################################################")
    else:
        ##################
        # check network
        ##################
        check_network = check_by_snmp(sys.argv[0])
        
    
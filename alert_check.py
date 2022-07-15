from hashlib import new
from ipaddress import ip_address
from wsgiref.simple_server import software_version
# from attr import attributes
from regex import R
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
from pprint import pprint

class nvr:

    def __init__(self,ip,port,user_name,password) -> None:
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password

    def payload_header_responce(self,url):
        payload={}
        headers = {
        'Cookie': 'secure'
        }
        response = requests.request("GET", url, headers=headers, data=payload,auth=HTTPDigestAuth(self.user_name,self.password))
        return response

    def get_url(self,sub_url):
        main_url = "http://"+self.ip + ":" + self.port +"/cgi-bin/"+sub_url
        return main_url

    def check_date_time(self): # Alert type 1: if date and time of nvr is not same as ntp server(online)/system (offline)
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nvr_date = None
        # print(today)
        
        sub_url = "global.cgi?action=getCurrentTime"
        responce = self.payload_header_responce(self.get_url(sub_url))
        new_responce = responce.text.rstrip().split("=")
        for i in new_responce:
            if i == "result":
                pass
            else:
                nvr_date = i
                
        if today == nvr_date:
            pass
        else:
            day = datetime.now().strftime("%Y-%m-%d")
            time = datetime.now().strftime("%H:%M:%S")
            url1 = "http://192.168.1.108/cgi-bin/global.cgi?action=setCurrentTime&time="+ day+"%20"+time
            responce = self.payload_header_responce(url1)

        return "Date is sync"


    def check_storage_exist(self): # Alert type 2: storage not exist
        sub_url = "storageDevice.cgi?action=getDeviceAllInfo"
        responce = self.payload_header_responce(self.get_url(sub_url))
        if len(responce.text) == 0:
            return("disk not connected")
        else:
            return("disk  connected")


    def check_storage_accessable(self):# Alert type 2: storage access failure 
        sub_url = "storageDevice.cgi?action=getDeviceAllInfo"
        responce = self.payload_header_responce(self.get_url(sub_url))
        data_list =[]
        data_dict = {}

        new_responce = responce.text.split(".")
        for i in new_responce:
            data_list.append(i.split("="))

        # print(final_data_list)
        for i in data_list:
            if i[0] == "TotalBytes":
                data_dict[i[0]] = i[1]

        if len(responce.text) == 0:
            return("disk not connected")
        else:
            print("disk  connected")
            for key,val in data_dict.items():
                val_int = int(val)
                if val_int == 0:
                    return("disk is bad")
                else:
                    return("disk is good") 


    def check_storage_space_low(self):# Alert type 2: storage space is low  
        sub_url = "storageDevice.cgi?action=getDeviceAllInfo"
        responce = self.payload_header_responce(self.get_url(sub_url))

        data_list =[]
        total_data_dict = {}
        used_data_dict ={}
        
        new_responce = responce.text.split(".")
        for i in new_responce:
            data_list.append(i.split("="))

        # print(final_data_list)
        for i in data_list:
            if i[0] == "TotalBytes":
                total_data_dict[i[0]] = i[1]
            elif i[0] == "UsedBytes":
                used_data_dict[i[0]] = i[1]

        for total_key,total_val in total_data_dict.items():
            for used_key,used_val in used_data_dict.items():
                # print(total_val,used_val)
                if total_val == used_val:
                    return("storage space low")
                else:
                    return("storage space not low")

    def check_video_loss(self):# Alert type 2: video loss
        sub_url = "configManager.cgi?action=getConfig&name=BlindDetect"
        responce = self.payload_header_responce(self.get_url(sub_url))
        return responce

    def check_video_blind(self):# Alert type 2: video blind
        sub_url = "configManager.cgi?action=getConfig&name=LossDetect"
        responce = self.payload_header_responce(self.get_url(sub_url))
        return responce

    def get_nvr_details(self):
        # sub_url ="storageDevice.cgi?action=getDeviceAllInfo"
        # responce = self.payload_header_responce(self.get_url(sub_url))
        # get device name
        get_device_name = "magicBox.cgi?action=getDeviceType"
        device_name = self.payload_header_responce(self.get_url(get_device_name))
        data_dict = {}
        device_name_list = device_name.text.split("=")
        device_name_dict = {}
        device_name_dict[device_name_list[0]] = device_name_list[1]

        #Get hardware version
        # get_hardware_version = "magicBox.cgi?action=getHardwareVersion"
        # device_version = self.payload_header_responce(self.get_url(get_hardware_version))
        # device_version_list = device_version.text.split("=")
        # device_version_dict = {}
        # device_version_dict[device_version_list[0]] = device_version_list[1]

        #Get serial number of device
        get_serial_number = "magicBox.cgi?action=getSerialNo"
        serial_number = self.payload_header_responce(self.get_url(get_serial_number))
        serial_number_list = serial_number.text.split("=")
        serial_number_dict = {}
        serial_number_dict[serial_number_list[0]] = serial_number_list[1]

        #Get machine name
        get_machine_name = "magicBox.cgi?action=getMachineName"
        machine_name = self.payload_header_responce(self.get_url(get_machine_name))
        machine_name_list = machine_name.text.split("=")
        machine_name_dict = {}
        machine_name_dict[machine_name_list[0]] = machine_name_list[1]

        # # Get system information
        # get_system_info = "magicBox.cgi?action=getSystemInfo"
        # system_info = self.payload_header_responce(self.get_url(get_system_info))
        # temp_system_info_list = system_info.text.rstrip().split("\r\n")
        # system_info_list = []
        # system_info_dict = {}
        # for i in temp_system_info_list:
        #     system_info_list.append(i.split("="))

        # for i in system_info_list:
        #     system_info_dict[i[0]] = i[1]

        # Get software version
        soft_version_dict = {}
        get_software_version = "magicBox.cgi?action=getSoftwareVersion"
        soft_version  = self.payload_header_responce(self.get_url(get_software_version ))
        soft_version_list = soft_version.text.split(",")
        soft_version_new = soft_version_list[0].split("=")
        soft_version_dict[soft_version_new[0]] = soft_version_new[1]


        # Get version of Onvif
        get_Onvif_version = "IntervideoManager.cgi?action=getVersion&Name=Onvif"
        Onvif_version  = self.payload_header_responce(self.get_url(get_Onvif_version))
        Onvif_version_list = Onvif_version.text.split("=")
        Onvif_version_dict = {}
        Onvif_version_dict[Onvif_version_list[0]] = Onvif_version_list[1]


        #get HDD info
        get_hdd_info = "storageDevice.cgi?action=getDeviceAllInfo"
        hdd_info = self.payload_header_responce(self.get_url(get_hdd_info))
       
        hdd_info_list = hdd_info.text.split()
        hdd_info_list_sub = []
        for i in hdd_info_list:
            hdd_info_list_sub.append(i.split("."))

        for i in hdd_info_list_sub:
            try:
                i[3]= i[3].split("=")
            except:
                i[2] = i[2].split("=")

        data_list = []
        static_data_dict = {}
        for i in hdd_info_list_sub:
            try:
                data_list.append([i[1],i[3]])
            except:
                data_list.append([i[1],i[2]])

        for i in data_list:
            static_data_dict[i[0]] = []

        for key,val in static_data_dict.items():
            for i in data_list:
                if key == i[0]:
                    val.append(i[1])
    
        info_data_dict = {}
        name_of_hdds ={}
        for key,val in static_data_dict.items():
            totalbytes_list = []
            usedbytes_list = []
            new_data_dict = {}
            for i in val:
                if i[0] == "TotalBytes":
                    totalbytes_list.append(int(i[1]))
                    new_data_dict[i[0]] = sum(totalbytes_list)
                elif i[0] == "UsedBytes":
                    usedbytes_list.append(int(i[1]))
                    new_data_dict[i[0]] = sum(usedbytes_list)
                elif i[0] == "Name":
                    name_of_hdds[key] = i[1]
            new_data_dict["UnusedBytes"] = new_data_dict["TotalBytes"] - new_data_dict["UsedBytes"]
            info_data_dict[name_of_hdds[key]] = new_data_dict
        
        
        data_dict["port"] = self.port
        data_dict["ip"] = self.ip
        data_dict["device_type"] = device_name_dict["type"].rstrip()
        # data_dict["hardware_version"] = device_version_dict["version"].rstrip()
        data_dict["serial_number"] = serial_number_dict["sn"].rstrip()
        # data_dict["machine_name"] = machine_name_dict["name"].rstrip()
        data_dict["software_version"] = soft_version_dict["version"]
        data_dict["Onvif_version"] = Onvif_version_dict["version"].rstrip()
        data_dict["HDD_details"] = info_data_dict
        return data_dict


    def check_nvr_status(self):
        status = ""
        try:
            sub_url = "magicBox.cgi?action=getMachineName"
            responce = self.payload_header_responce(self.get_url(sub_url))
            status = "NVR ON"
        except:
            status = "NVR OFF"
        return status
        

# n1 = NVR("192.168.1.108","80","admin","admin123")

# responce = n1.check_date_time()
# print(responce)

# responce = n1.check_storage_exist()
# print(responce)

# responce = n1.check_storage_accessable()
# print(responce)

# responce = n1.check_storage_space_low()
# print(responce)

# responce = n1.get_nvr_details()
# print(responce)

# responce = n1.check_nvr_status()
# print(responce)

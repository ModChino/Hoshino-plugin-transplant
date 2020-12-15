import psutil
import requests
from datetime import datetime
from hoshino import log

logger = log.new_logger('check')

class Check():
    def __init__(self, request_name_list={}):
        self.request_name_list = request_name_list
        self.cpu_percent = 0
        self.memory_percent = 0
        self.disk_percent = 0
        self.boot_time = 0
        self.send = 0
        self.recv = 0
        self.packets_sent = 0
        self.packets_recv = 0
        self.packet_lost = 0
        self.baidu = 404
        self.google = 404
        self.process_name_list = []
        self.process_status_list = []
        self.user_list =[]
        self.run_all_check()

    def run_all_check(self):
        self.get_performance_check()
        self.get_network_check()
        self.get_process_status(self.request_name_list)
        self.get_users_check()

    async def get_check_info(self):
        self.run_all_check()
        putline = []
        putline.append("--Performance--\n[Cpu] {}%\n[Memory] {}%\n[Disk] {}%\n[Boot time] {}\n--Network--\n[Send] {}MB\n[Receive] {}MB\n[Packets sent] {}\n[Packets recv] {}\n[Packets lost] {}%".format(self.cpu_percent, self.memory_percent, self.disk_percent, self.boot_time, self.send, self.recv, self.packets_sent, self.packets_recv, self.packet_lost))        
        if self.process_name_list:
            putline.append("--Process--")
            for name, status in zip(self.process_name_list, self.process_status_list):
                putline.append("[{}] {}".format(name, status))      
        if self.user_list:
            putline.append("--Users--")
            for user in self.user_list:
                putline.append("[{}] {}".format(user['name'], user['started']))       
        return "\n".join(putline)

    async def get_check_easy(self, max_performance_percent=[92,92,92]):
        self.run_all_check()
        putline = []
        check_list = await self.get_check_simple()
        if sum(check_list) != 0:
            logger.error("Computer problem detected. check code: {}".format(check_list))
            if sum(check_list) == 5:
                return "我去世了……（安详\n⚠请在群聊中发送自检指令获取详细信息"
            if sum(check_list) == 4:
                return "如果还能看到消息那一定是奇迹……\n⚠请在群聊中发送自检指令获取详细信息"
            if sum(check_list[:3]) != 0:
                return "啊……我感觉……好热……\n⚠请在群聊中发送自检指令获取详细信息"
            if check_list[4] == 1:
                return "我节点断了……(部分功能会受到影响)"
        else:
            putline.append("当前网络状态：\n上传：{}MB\n接收：{}MB\n丢包率: {}%\n※请留意服务器的运行状态".format(self.send, self.recv, self.packet_lost))
            return "\n".join(putline)

    async def get_check_simple(self, max_performance_percent=[92,92,92]) -> list:
        check_list = [0,0,0,0,0,0]
        self.run_all_check()
        if self.cpu_percent > max_performance_percent[0]:
            check_list[0] = 1
        if self.memory_percent > max_performance_percent[1]:
            check_list[1] = 1
        if self.disk_percent > max_performance_percent[2]:
            check_list[2] = 1
        if self.baidu != 200:
            check_list[3] = 1
        if self.google != 200:
            check_list[4] = 1
        for status in self.process_status_list:
            if status != 'running':
                check_list[5] = 1
                break      
        return check_list

    def get_performance_check(self):
        self.cpu_percent = psutil.cpu_percent()
        self.memory_percent = psutil.virtual_memory().percent
        self.disk_percent = psutil.disk_usage("/").percent
        self.boot_time = datetime.fromtimestamp(
        psutil.boot_time()).strftime("%Y-%m-%d %H: %M: %S")

    def get_network_check(self):
        self.send = round(psutil.net_io_counters().bytes_sent/1024/1024, 2)
        self.recv = round(psutil.net_io_counters().bytes_recv/1024/1024, 2)
        self.packets_sent = psutil.net_io_counters().packets_sent
        self.packets_recv = psutil.net_io_counters().packets_recv
        self.packet_lost = round(
        psutil.net_io_counters().packets_recv / psutil.net_io_counters().packets_sent, 2
    )
        try:
            self.baidu = requests.get("http://www.baidu.com").status_code
        except:
            self.baidu = 404
            logger.warning("Baidu request failed.")

        try:
            self.google = requests.get("http://www.google.com").status_code
        except:
            self.google = 404
            logger.warning("Google request failed.")
            
    def get_users_check(self):
        user_list = []
        suser_l = psutil.users()

        for suser in suser_l:
            user = {
                'name': suser.name, 
                'started': datetime.fromtimestamp(suser.started).strftime("%Y-%m-%d %H:%M:%S")}
            user_list.append(user)

        self.user_list = user_list

    def get_process_status(self, request_name_list: set):
        if not request_name_list:
            return None
        
        self.process_name_list = []
        self.process_status_list = []
        
        for p_n in request_name_list:
            p_l = self.get_sname_process_list(p_n)
            if len(p_l) == 1:
                self.process_name_list.append(p_n)
                self.process_status_list.append(p_l[0].status())
            else:
                for i, p in enumerate(p_l):
                    self.process_name_list.append(p_n+" ({})".format(i))
                    self.process_status_list.append(p.status())

    @staticmethod
    def get_sname_process_list(name: str) -> list:
        p_l = []
        pids  = psutil.pids()

        for pid in pids:
            p = psutil.Process(pid)
            if (p.name() == name):
                p_l.append(p)

        return p_l
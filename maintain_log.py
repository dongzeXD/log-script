import time
import re
import os
import configparser

re_date = r"^\d{4}-\d{1,2}-\d{1,2}"
re_log = r"^\d{4}-\d{1,2}-\d{1,2}.log$"
config_file = r"script_config.ini"




class maintain_log:
    cf = configparser.ConfigParser()
    cf.read(config_file)

    def __init__(self):

        self.out_time = int(self.cf.get("log", "out_time"))     # 读取日志文件过期时间
        self.log_file_dir = self.cf.get("log", "log_dir")  # 读取日志文件存放目录
        self.script_log_file = self.cf.get("log", "script_log_file")  # 读取脚本执行日志文件
        
        self.file_list = [logfile_w_time for logfile_w_time in  os.listdir(self.log_file_dir) if re.match(re_log, logfile_w_time) is not None]
        print(self.file_list)
        self.file_dict = self._file_gather()

    def _file_gather(self):
        return {re.match(re_date, fileName).group(): os.path.join(self.log_file_dir, fileName) for fileName in self.file_list}

    def _file_outdate(self, date_str: str):
        time_ago = time.strptime(date_str, '%Y-%m-%d')
        time_now = time.localtime()
        hash_time_now = time.mktime(time_now)
        hash_time_ago = time.mktime(time_ago)
        sub_day = (hash_time_now - hash_time_ago) / (24* 60* 60)
        return sub_day > self.out_time

    def _p2log(self, log_str: str):
        try:
            with open(self.script_log_file, 'a') as f:
                f.write(log_str)
        except FileNotFoundError as e:
            print("\033[31mFile open error!\033[0m")
            print(e)

    def delate(self):
        for lfile, lfdir in self.file_dict.items():
            if self._file_outdate(lfile) == 1 and os.path.exists(lfdir):
                os.remove(lfdir)   
                self._p2log(lfdir + " have been removed " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
                


ml = maintain_log()
ml.delate()



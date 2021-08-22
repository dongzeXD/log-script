import configparser
import os, sys
import time
import re

# 用数据库名称+ y-m-d + .sql
re_date = r"\d{4}-\d{1,2}-\d{1,2}"
re_sql = r"\d{4}-\d{1,2}-\d{1,2}.sql$"
config_file = r"script_config.ini"


class maintain_sql:
    cf = configparser.ConfigParser()
    cf.read(config_file)

    def __init__(self):
        global re_sql

        self.out_time = int(self.cf.get("sql", "out_time"))     # 读取过期时间
        self.backup_file = self.cf.get("sql", "backup2")        # 备份目录
        self.script_log_file = self.cf.get("sql", "script_log_file")  # 维护脚本日志文件
        self.db_name = self.cf.get("sql", "database_name")      # 需备份数据库名

        re_sql = "^" + self.db_name + '-' + re_sql

        self.file_list = [sqlfile_w_time for sqlfile_w_time in  os.listdir(self.backup_file) if re.match(re_sql, sqlfile_w_time) is not None]
        self.file_dict = self._file_gather()

    def _file_gather(self):
        return {re.search(re_date, fileName).group(): os.path.join(self.backup_file, fileName) for fileName in self.file_list}

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
                self._p2log(lfdir+ " have been removed " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")

    @classmethod
    def backup_sql(cls):
        backup_file = cls.cf.get("sql", "backup2")
        backup_db = cls.cf.get("sql", "database_name")
        script_log = cls.cf.get("sql", "script_log_file")
        dumpcmd = "mysqldump -u root -p{password}  {dbname} > {backup_file}/{dbname}-{backup_time}.sql".format(dbname=backup_db, backup_file=backup_file, backup_time=time.strftime('%Y-%m-%d'), password="123456")
        code = os.system(dumpcmd)
        try:
            with open(script_log, 'a') as f:
                f.write("command execute " + dumpcmd + "\n" + "Code:" + str(code)+ "  " +time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
        except Exception:
            print("\033[31mFile open error!\033[0m")


if __name__ == "__main__":
    if sys.argv[1] == '0':
        ms = maintain_sql()
        ms.delate()
    else:
        maintain_sql.backup_sql()

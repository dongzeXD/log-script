# use in linux
update script_config.ini

    sudo vim /etc/crontab
Insert these below

50 23   * * *   root   	/usr/bin/python3 /your/directory/maintain_log.py

0   0   1 * * 	root	/usr/bin/python3 /your/directory/backup_mysql.py 1

0   0   1 * *	root	/usr/bin/python3 /your/directory/backup_mysql.py 0

-----
crontab rules:

    * * * * * user command
    Minutes Hours Days Months Weeks     

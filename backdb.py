from subprocess import call
from datetime import datetime

current_time = datetime.now()
filename = str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_recruit.sqlite3'
call(["cp", "../db_recruit.sqlite3", filename])
call(["rsync", "-avzhe", "ssh", filename, "hao@123.206.196.147:dbbackup"])
call(["rm", filename])

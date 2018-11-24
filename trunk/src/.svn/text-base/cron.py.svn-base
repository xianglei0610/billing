# -*- coding: utf-8 -*-

from apscheduler.scheduler import Scheduler
from dao import dbop

@dbop
def create_table_call_log():
    from models import Call_Log_Next
    from models import T_Callstat_Next
    Call_Log_Next.create_table(True)
    T_Callstat_Next.create_table(True)

def main():
    sched = Scheduler()
    #添加定时任务
    sched.add_interval_job(create_table_call_log, hours=4)
    sched.start()

if __name__ == '__main__':
    main()

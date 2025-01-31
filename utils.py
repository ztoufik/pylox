from enum import Enum

class Result(Enum):
    Ok=1
    err=2

class Ilogger:

    def report(self,line_num,where_str,msg_str):
        print(f"[line {line_num}] Error {where_str} : {msg_str}")
        self.haderror=True

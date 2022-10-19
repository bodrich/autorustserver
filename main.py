from app.rcon_client import RCONClient
from app.scheduler import Scheduler

if __name__ == '__main__':
    RCONClient().kickall()
    #Scheduler().run()

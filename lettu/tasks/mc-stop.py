import hikari
import lightbulb
import os
import time
from lightbulb.ext import tasks
from mcstatus import JavaServer
from lettu import credentials


server = JavaServer.lookup(f"{credentials.MC_DOM}:25565")

plugin = lightbulb.Plugin("mc_stop")

@tasks.task(tasks.CronTrigger('0/15 8-23,0-1 * * *'), auto_start=True)
async def mc_stop():
    try:
        server.ping()
        status = 0
        print("Server is up")
        online = server.status().players.online
        print(f"Online: {online}")
    except:
        status = 1
        print("Server is down")
    if status == 0 and online == 0:
        print("test")
        minutes = 0
        while online == 0:
            if minutes == 5:
                print("Shutting down...")
                os.system(f"ssh {credentials.USER}@{credentials.MC_IP} sudo shutdown now")
                return
            else:
                try:
                    server.ping()
                    online = server.status().players.online
                    print(f"Online: {online}")
                    minutes += 1
                    time.sleep(60)
                    print(f"Minutes: {minutes}")
                except:
                    print("Server unreachable, exiting...")
                    return
        print("Server not empty, exiting...")
        return


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
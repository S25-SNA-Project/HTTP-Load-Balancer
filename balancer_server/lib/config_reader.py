import json
from lib.servers_heap import ServersHeap
from os import getcwd
from os.path import join, curdir

with open("config.json", "r") as file:
    config = json.load(file)
servers_queue: ServersHeap = ServersHeap()
async def configure_queue():
    for server in config["servers"]:
        await servers_queue.push(server, 0)
    print(config)
    print(servers_queue)
import json
from lib.servers_heap import ServersHeap
from os import getcwd
from os.path import join, curdir

with open("balancer_server/config.json", "r") as file:
    config = json.load(file)
servers_queue: ServersHeap = ServersHeap()
for server in config["servers"]:
    servers_queue.push((0, server))  
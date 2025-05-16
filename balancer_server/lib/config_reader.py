import json
from pathlib import Path
from lib.servers_heap import ServersHeap
from logging import getLogger, INFO, StreamHandler, Formatter


with open("config.json", "r") as file:
    config = json.load(file)

for path_part in Path(config["log_file"]).parents:
    if not path_part.exists():
        path_part.mkdir(parents=True, exist_ok=True)

chanel = StreamHandler(open(config["log_file"], "a"))
chanel.setFormatter(Formatter(
            "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
chanel.setLevel(INFO)

logger = getLogger("custom_logger")
logger.setLevel(INFO)
logger.addHandler(chanel)

servers_queue: ServersHeap = ServersHeap()
async def configure_queue():
    for server in config["servers"]:
        await servers_queue.push(server, 0)
    logger.info(f"Servers queue configured with {len(servers_queue)} servers.")
    logger.info(f"Servers queue: {servers_queue}")
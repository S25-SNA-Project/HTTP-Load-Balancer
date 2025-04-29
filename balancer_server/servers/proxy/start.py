from uvicorn import run
from asyncio import run as aRun
from .reverse_proxy import reverse_proxy
from lib.config_reader import config, configure_queue

def start():
    aRun(configure_queue(), debug=False)
    run(reverse_proxy, port=config["exposed_port"])
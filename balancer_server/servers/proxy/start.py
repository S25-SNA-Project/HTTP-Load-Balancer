from uvicorn import run
from reverse_proxy import reverse_proxy
from lib.config_reader import config

def start():
    run(reverse_proxy, port=config["exposed_port"])
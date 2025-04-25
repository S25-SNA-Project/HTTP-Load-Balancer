import time
from threading import Thread

from uvicorn import Config, Server
from lib.config_reader import config
from servers.reverse_proxy import reverse_proxy
from servers.servers_communicator import communicator


if __name__ == "__main__":
    server1 = Server(Config(reverse_proxy, port=config["exposed_port"]))
    server2 = Server(Config(communicator, port=config["balancing_port"]))

    t1 = Thread(target=server1.run, daemon=True)
    t2 = Thread(target=server2.run, daemon=True)

    t1.start()
    t2.start()

    try:
        while True: time.sleep(1000)
    except KeyboardInterrupt:
        print("Shutdown requested, stopping servers…")
        server1.should_exit = True
        server2.should_exit = True
        t1.join()
        t2.join()
        print("✅ Servers stopped")

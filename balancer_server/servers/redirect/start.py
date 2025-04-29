import asyncio
import signal

from uvicorn import Config, Server
from lib.config_reader import config
from servers.redirect.reverse_proxy import reverse_proxy
from servers.redirect.servers_communicator import communicator
from lib.config_reader import configure_queue

async def serve(app, port):
    server = Server(Config(app, port=port))
    await server.serve()

async def main():
    await configure_queue()  
    tasks = [
        asyncio.create_task(serve(reverse_proxy, config["exposed_port"])),
        asyncio.create_task(serve(communicator, config["balancing_port"]))
    ]

    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set_result, None)

    await stop  # wait until one of the signals arrives
    print("Shutdown requested, stopping servers…")

    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    print("✅ Servers stopped")

def start():
    asyncio.run(main(), debug=False)

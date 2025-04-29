from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from lib.config_reader import servers_queue, config
from aiohttp.client import request as aRequest
from uvicorn import run

communicator = FastAPI()
communicator.add_middleware(
    CORSMiddleware,
    allow_origins=["http://" + x for x in config['servers']] + ["https://" + x for x in config['servers']],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@communicator.post("/finish")
async def handle_finish(request: Request):
    server_ip = request.client.host
    # temporary fix, brakes if all applications works on localhost
    # TODO: ID system for servers
    addr = config['servers'].index(lambda x: server_ip in x.split(':')[0])
    if addr == -1:
        return Response(status_code=403, content=f"{server_ip} is not registered as a worker")
    addr = config['servers'][addr]
    # end of temporary fix
    await servers_queue.update_load(server_ip, max((await servers_queue[addr]).load - 1, 0))
    return Response(status_code=200, content=f"{server_ip}")

@communicator.post("/connect")
async def handle_connect(request: Request):
    # TODO security improvements to be unable to connect from any server and re
    server_ip = request.client.host
    server_port = request.query_params.get("port")
    if server_port is None:
        return Response(status_code=400, content="Port not specified")
    server_ip = f"{server_ip}:{server_port}"
    servers_queue.push(server_ip, 0)
    return Response(status_code=200, content=f"{server_ip}")

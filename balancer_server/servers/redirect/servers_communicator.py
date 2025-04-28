from fastapi import FastAPI, Request
from fastapi.responses import Response
from lib.config_reader import servers_queue
from aiohttp.client import request as aRequest
from uvicorn import run

communicator = FastAPI()

@communicator.post("/finish")
async def handle_finish(request: Request):
    server_ip = request.client.host
    servers_queue[server_ip] = servers_queue[server_ip].load - 1
    return Response(status_code=200, content=f"{server_ip}")


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
    await servers_queue.update_load(server_ip, max((await servers_queue[server_ip]).load - 1, 0))
    return Response(status_code=200, content=f"{server_ip}")


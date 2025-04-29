from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from lib.config_reader import servers_queue
from aiohttp.client import request as aRequest
from lib.config_reader import logger

reverse_proxy = FastAPI()
reverse_proxy.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@reverse_proxy.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):
    logger.info(f"Client request to {request.method} {full_path} from {request.client.host}")
    optimal_node = servers_queue.peek()
    servers_queue.update_root(optimal_node.load + 1)
    full_path = full_path.lstrip("/")
    logger.info(f"Redirecting to {optimal_node.ip}")
    response = await aRequest(
        request.method,
        f"http://{optimal_node.ip}/{full_path}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )
    logger.info(f"Response from {optimal_node.ip} obtained. Responding to client.")
    res = Response(
        status_code=response.status,
        content=await response.read(),
        headers=response.headers
    )
    servers_queue[optimal_node.ip] = servers_queue[optimal_node.ip] - 1
    return res

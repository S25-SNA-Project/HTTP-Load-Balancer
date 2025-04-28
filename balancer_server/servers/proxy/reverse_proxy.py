from fastapi import FastAPI, Request
from fastapi.responses import Response
from lib.config_reader import servers_queue
from aiohttp.client import request as aRequest

reverse_proxy = FastAPI()

@reverse_proxy.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):
    optimal_node = servers_queue.peek()
    servers_queue.update_root(optimal_node.load + 1)
    full_path = full_path.lstrip("/")
    response = await aRequest(
        request.method,
        f"http://{optimal_node.ip}/{full_path}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )
    res = Response(
        status_code=response.status,
        content=await response.read(),
        headers=response.headers
    )
    servers_queue[optimal_node.ip] = servers_queue[optimal_node.ip] - 1
    return res



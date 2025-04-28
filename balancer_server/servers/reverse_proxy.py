from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from lib.config_reader import servers_queue
from aiohttp.client import request as aRequest

reverse_proxy = FastAPI()

@reverse_proxy.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):
    while True:
        optimal_node = servers_queue.peek()
        ack = await aRequest(
            "POST",
            f"http://{optimal_node[1]}", 
            data={"client_ip": request.client.host}, 
            timeout=.1
        )
        if ack.status > 300:
            servers_queue.pop()
            continue
        break
    servers_queue.update_root(ack.data["load"])
    return RedirectResponse(optimal_node[1] + "/" + full_path, status_code=307)



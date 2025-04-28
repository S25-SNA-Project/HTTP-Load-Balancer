from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from lib.config_reader import servers_queue
from aiohttp.client import request as aRequest

reverse_proxy = FastAPI()

@reverse_proxy.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):
    while True:
        optimal_node = await servers_queue.peek()
        ack = await aRequest(
            "POST",
            f"http://{optimal_node.ip}", 
            data={"client_ip": request.client.host}, 
            timeout=.1
        )
        if ack.status > 300:
            await servers_queue.pop()
            continue
        break
    await servers_queue.update_root(ack.data["load"])
    return RedirectResponse(optimal_node.ip + full_path, status_code=307)



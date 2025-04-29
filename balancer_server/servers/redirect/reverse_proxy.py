from lib.config_reader import logger
from json import loads
from aiohttp import ClientConnectorError, ClientTimeout
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from lib.config_reader import servers_queue
from aiohttp import ClientSession

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

    while True:
        optimal_node = await servers_queue.peek()
        try:
            async with ClientSession() as session:
                print(f"http://{optimal_node.ip}/tasks_count")
                ack = await session.request(
                    "POST",
                    # "GET",
                    f"http://{optimal_node.ip}/tasks_count", 
                    json={"client_ip": str(request.client.host).split(':')[0]},
                    timeout=ClientTimeout(total=1),
                )
            # if ack.status > 300:
            #     await servers_queue.pop()
            #     continue
        except ClientConnectorError:
            logger.error(f"Server {optimal_node.ip} is down, removing from queue. Trying next instance.")
            await servers_queue.pop()
            continue
        break
    await servers_queue.update_root(loads(await ack.text())["active_tasks"] + 1)
    logger.info(f"Redirecting to {optimal_node.ip}")
    return RedirectResponse(f"http://{optimal_node.ip}/{full_path.lstrip('/')}?{'&'.join(f'{k}={request.query_params[k]}' for k in request.query_params)}", status_code=307)



from aiohttp import ClientSession, ClientTimeout, ClientConnectorError
from asyncio import TimeoutError
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from json import loads
from lib.config_reader import logger, servers_queue

reverse_proxy = FastAPI()
reverse_proxy.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@reverse_proxy.get("/favicon.ico", include_in_schema=False)
async def no_favicon():
    return Response(status_code=204)


@reverse_proxy.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, full_path: str):
    logger.info(f"Client request to {request.method} {full_path} from {request.client.host}")

    timeout = ClientTimeout(total=5) 
    async with ClientSession(timeout=timeout) as session:
        while True:
            optimal_node = await servers_queue.peek()
            url = f"http://{optimal_node.ip}/tasks_count"
            try:
                async with session.post(
                    url,
                    json={"client_ip": request.client.host},
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
            except (ClientConnectorError, TimeoutError):
                logger.error(f"Server {optimal_node.ip} down, pop and retry")
                await servers_queue.pop()
                continue
            except Exception as e:
                body = await resp.text() if 'resp' in locals() else "<no response>"
                raise RuntimeError(f"Error getting tasks_count from {url}: {e}, body={body!r}")
            await servers_queue.update_root(data["active_tasks"] + 1)
            break

    logger.info(f"Redirecting to {optimal_node.ip}")
    qs = "&".join(f"{k}={v}" for k, v in request.query_params.items())
    return RedirectResponse(f"http://{optimal_node.ip}/{full_path.lstrip('/')}?{qs}", status_code=307)

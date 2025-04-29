import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from uvicorn import run
from config import BALANCER_ADDR, APPLICATION_PORT, BALANCER_PORT, logger


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_tasks = 0
active_waiting_clients = set()
lock = asyncio.Lock()

@app.post("/tasks_count")
async def tasks_count(request: Request):
    logger.info(f"Request to /tasks_count from {request.client.host}")
    if str(request.client.host).split(':')[0] != BALANCER_ADDR.split(':')[0]:
        logger.error(f"Request to /tasks_count from {request.client.host} is not from the proxy server.")
        raise HTTPException(
            status_code=403,
            detail="This endpoint is only accessible from the proxy server.",
        )
    body = await request.body()

    data = json.loads(body)
    client_ip = data.get("client_ip")

    active_waiting_clients.add(client_ip)

    logger.info(f"Client {client_ip} successfully registered and added to the await queue.")
    return {"active_tasks": active_tasks}



@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(full_path: str, _request: Request):
    global active_tasks
    logger.info(f"Client request [{_request.method} {full_path}] from {_request.client.host}")
    if str(_request.client.host).split(':')[0] not in active_waiting_clients:
        logger.error(f"Request from {str(_request.client.host).split(':')[0]} is not awaited. Redirect to be balanced.")
        return RedirectResponse(
            f"http://{BALANCER_ADDR}/{full_path.lstrip('/')}",
            status_code=307,
        )
    async with lock:
        active_tasks += 1

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            url = f"http://127.0.0.1:{APPLICATION_PORT}/{full_path}"
            method = _request.method
            headers = dict(_request.headers)
            body = await _request.body()

            params = dict(_request.query_params)
            response = await client.request(method, url, headers=headers, content=body, params=params)
            res = JSONResponse(
                status_code=response.status_code,
                content=response.json() if "application/json" in response.headers.get("content-type", "") else {
                    "response": response.text},
            )
        logger.info(f"Response from {APPLICATION_PORT} obtained. Transmitting information about end to the balancer.")
        async with httpx.AsyncClient(timeout=None) as client:
            await client.post(
                f"http://{BALANCER_ADDR}/finish",
            )
        logger.info(f"Response from {APPLICATION_PORT} sent to the client.")
        return res
    except:
        print(full_path)
    finally:
        async with lock:
            active_tasks -= 1
            active_waiting_clients.remove(str(_request.client.host).split(':')[0])


if __name__ == "__main__":
    with httpx.Client() as client:
        client.post(
            f"http://{BALANCER_ADDR}/connect",
            params={"port": BALANCER_PORT},
        )
    logger.info(f"Connected to balancer at {BALANCER_ADDR}.")
    run(
        app,
        port=BALANCER_PORT
    )
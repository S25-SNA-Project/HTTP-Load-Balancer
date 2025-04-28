from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import asyncio

app = FastAPI()
active_tasks = 0
lock = asyncio.Lock()


@app.get("/tasks_count")
async def tasks_count():
    return {"active_tasks": active_tasks}


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(full_path: str, _request: Request):
    global active_tasks

    async with lock:
        active_tasks += 1

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            url = f"http://127.0.0.1:8888/{full_path}"
            method = _request.method
            headers = dict(_request.headers)
            body = await _request.body()

            params = dict(_request.query_params)
            response = await client.request(method, url, headers=headers, content=body, params=params)

            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if "application/json" in response.headers.get("content-type", "") else {
                    "response": response.text},
            )

    finally:
        async with lock:
            active_tasks -= 1

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

counter = 0

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello world</h1>"

@app.get("/prime")
def add_numbers(a: int):
    cnt = 0
    for i in range(1, a+1):
        if a % i == 0:
            cnt += 1
    return {"result": cnt}


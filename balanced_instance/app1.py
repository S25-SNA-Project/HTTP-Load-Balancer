from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="./static/html"),
    name="static",
)

counter = 0

@app.get("/")
async def read_root() -> HTMLResponse:
    return HTMLResponse('\n'.join(open("./static/hello_w.html", 'r').readlines()))

@app.get("/media_example")
async def media_example():
    return FileResponse("static/TheLittlePrince.pdf", media_type="application/pdf")

@app.get("/prime/{a}")
def add_numbers(a: int):
    cnt = 0
    for i in range(1, a+1):
        if a % i == 0:
            cnt += 1
    return {"result": cnt}


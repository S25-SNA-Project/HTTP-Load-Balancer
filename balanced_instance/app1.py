from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

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
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

counter = 0

@app.get("/")
async def read_root() -> HTMLResponse:
    return HTMLResponse('\n'.join(open(STATIC_DIR / "hello_w.html", 'r').readlines()))

@app.get("/media_example")
async def media_example():
    file_path = STATIC_DIR / "TheLittlePrince.pdf"
    return FileResponse(file_path, media_type="application/pdf")

@app.get("/prime/{a}")
def add_numbers(a: int):
    cnt = 0
    for i in range(1, a+1):
        if a % i == 0:
            cnt += 1
    return {"result": cnt}


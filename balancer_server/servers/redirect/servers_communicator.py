from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from lib.config_reader import servers_queue, config
from lib.config_reader import logger

communicator = FastAPI()
communicator.add_middleware(
    CORSMiddleware,
    allow_origins=["http://" + x for x in config['servers']] + ["https://" + x for x in config['servers']],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@communicator.post("/finish")
async def handle_finish(request: Request):
    logger.info(f"Received finish of single task by instance on {request.client.host}")

    server_ip = request.client.host
    # temporary fix, brakes if all applications works on localhost
    # TODO: ID system for servers
    addr = -1
    for i, server in enumerate(config['servers']):
        if server_ip in server:
            addr = i
            break
    if addr == -1:
        logger.info(f"Instance {request.client.host} is not a registered worker")
        return Response(status_code=403, content=f"{server_ip} is not registered as a worker")
    addr = config['servers'][addr]
    # end of temporary fix
    await servers_queue.update_load(server_ip, max((await servers_queue[addr]).load - 1, 0))
    return Response(status_code=200, content=f"{server_ip}")

@communicator.post("/connect")
async def handle_connect(request: Request):
    logger.info(f"Received request to register instance located on {request.client.host}")

    # TODO security improvements to be unable to connect from any server and intercept the requests
    server_ip = request.client.host
    server_port = request.query_params.get("port")
    if server_port is None:
        logger.error(f"Malformed register request from {server_ip}")
        return Response(status_code=400, content="Port not specified")
    server_addr = f"{server_ip}:{server_port}"
    await servers_queue.push(server_addr, 0)
    config['servers'].append(server_addr)

    logger.info(f"Successfully register request-handling instance located on {request.client.host}")
    return Response(status_code=200, content=f"OK")

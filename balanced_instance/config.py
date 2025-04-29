import argparse
import json
from os import getenv

from logging import getLogger, INFO, StreamHandler, Formatter

parser = argparse.ArgumentParser(
    description="FastAPI proxy (you can override application_port on the CLI)"
)
parser.add_argument(
    "--config-file",
    type=str,
    default="config.json",
    help="path to config JSON",
)
parser.add_argument(
    "--application-port",
    type=int,
    default=None,
    help="the port of the backend application (overrides config.json)",
)
parser.add_argument(
    "--balanced-port",
    type=int,
    default=None,
    help="the port to communicate with the balancer (overrides config.json)",
)
parser.add_argument(
    "--balancer-addr",
    type=str,
    default=None,
    help="the balancer address (overrides config.json)",
)
args, _ = parser.parse_known_args()


with open(args.config_file, "r") as file:
    config = json.load(file)

if args.application_port:
    config["application_port"] = args.application_port
if args.balancer_addr:
    config["balancing_address"] = args.balancer_addr
if getenv("balancer-addr", None) is not None:
    config["balancing_address"] = getenv("balancer-addr", None)
if args.balanced_port:
    config["balanced_port"] = args.balanced_port
BALANCER_ADDR = config["balancing_address"]
APPLICATION_PORT = config["application_port"]
BALANCER_PORT = config["balanced_port"]

chanel = StreamHandler(open(config["log_file"], "a"))
chanel.setFormatter(Formatter(
            "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
chanel.setLevel(INFO)

logger = getLogger("custom_logger")
logger.setLevel(INFO)
logger.addHandler(chanel)

from servers.redirect.start import start as rStart
from servers.proxy.start import start as pStart
from lib.config_reader import config

if __name__ == "__main__":
    match config["type"]:
        case "proxy":
            pStart()
        case "redirect":
            rStart()
        case _:
            raise RuntimeError(f"Unknown server type: {config["type"]}")

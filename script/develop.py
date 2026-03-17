# #! ./.venv/bin/python 

from pathlib import Path 
import asyncio
import os
import subprocess
from dotenv import load_dotenv
import signal

root_path = Path(__file__).resolve().parent.parent

load_dotenv(f"{root_path}/packages/database/.env")

_CONTAINER_NAME = "db_dev_env"
_USER = "POSTGRES_USER"
_PASS = "POSTGRES_PASSWORD"
_DB = "POSTGRES_DB"

async def task(command: list[str]):
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while 1:
        each_line = await proc.stdout.readline()
        if not each_line:
            break
        print(each_line.decode().strip()) 

async def main_runtime():
    tasks = [
        asyncio.create_task(task(["pnpm","run",f"--prefix={root_path}/backend","start:dev"])),
        asyncio.create_task(task(["docker","run","--rm",
        "--name",_CONTAINER_NAME,
        "-e",_PASS+"="+os.getenv(_PASS),
        "-e",_USER+"="+os.getenv(_USER),
        "-e",_DB+"="+os.getenv(_DB),
        "-p","5432:5432",
        "-v",f"{root_path}/var:/var/lib/postgresql:Z",
        "postgres:latest"]))
    ]

    loop = asyncio.get_running_loop()

    def cancel():
        for task in tasks:
            task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig,cancel)

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("stopping database environment ...")
        subprocess.run(["docker","stop",_CONTAINER_NAME])
        print("All tasks has stopped !!")
    
asyncio.run(main_runtime())
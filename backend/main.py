import os
import socket
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INSTANCE_NAME = os.environ.get("INSTANCE_NAME", socket.gethostname())


@app.get("/api/hello")
def read_hello():
    return {
        "message": f"Hello from FastAPI! (served by {INSTANCE_NAME})",
        "instance": INSTANCE_NAME,
        "hostname": socket.gethostname(),
    }

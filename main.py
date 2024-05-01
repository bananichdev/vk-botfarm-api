import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import app as api_v1
from settings import ALLOW_ORIGIN, HOST, PORT

app = FastAPI()
app.mount("/api/v1/botfarm", api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=[ALLOW_ORIGIN],
    allow_credentials=True,
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host=HOST, port=PORT)

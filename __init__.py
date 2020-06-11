from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8000/login",
    "http://localhost:8000/signup",
    "http://localhost:63342/fastCRM/index.html?_ijt=o1d8ejskjtra8k0331vg4jjrnc#:1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from .controllers.index import login
from .controllers.index import signup
from .controllers.index import login

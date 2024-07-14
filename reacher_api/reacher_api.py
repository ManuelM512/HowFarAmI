from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import reach_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Links(BaseModel):
    from_link: str
    to_link: str


@app.post("/reach")
def reacher(links: Links):
    from_link = links.from_link[24:]
    to_link = links.to_link[24:]
    return reach_service.reach(from_link, to_link)

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import reach_service

app = FastAPI()


class Links(BaseModel):
    from_link: str
    to_link: str


@app.post("/reach/")
def reacher(links: Links):
    from_link = links.from_link
    to_link = links.to_link
    return PlainTextResponse(reach_service.reach(from_link, to_link))

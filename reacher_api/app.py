from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Links
import reach_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/reach")
def reacher(links: Links):
    from_link = links.from_link
    to_link = links.to_link
    return reach_service.reach(from_link, to_link)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

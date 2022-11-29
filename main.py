import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import superset

load_dotenv()

DASHBOARD_ID = os.getenv("DASHBOARD_ID")
SUPERSET_DOMAIN = os.getenv("SUPERSET_DOMAIN")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/guest-token")
async def analytics_view(request: Request):
    access_token = superset.authenticate()
    guest_token = superset.get_guest_token_for_dashboard(
        dashboard_id=DASHBOARD_ID, access_token=access_token
    )
    return guest_token


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "DASHBOARD_ID": DASHBOARD_ID,
            "SUPERSET_DOMAIN": SUPERSET_DOMAIN,
        },
    )

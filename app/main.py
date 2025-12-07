from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from .db import init_db, get_session
from .routers import weather, ephemerides, dashboard, news

app = FastAPI(title="HomeDash MVP")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(weather.router)
app.include_router(ephemerides.router)
app.include_router(dashboard.router)
app.include_router(news.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
def startup():
    init_db()

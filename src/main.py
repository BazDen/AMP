from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from translate import get_labels, get_languages
import config

app = FastAPI(title="AMP", description="AMP", version="0.3")
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get("/")
@app.get("/{language:str}/{layout:int}/")
async def root(
    request: Request,
    language: str = config.default_language,
    layout: int = config.default_layout,
):
    content = {
        "show_layout": True,
        "show_settings": True,
        "show_menu": True,
        "path": "index",
        "layout": layout,
        "labels": get_labels(language),
        "languages": get_languages(),
        "language": language,
    }

    return templates.TemplateResponse(
        name="index.html", context={"request": request, "content": content}
    )

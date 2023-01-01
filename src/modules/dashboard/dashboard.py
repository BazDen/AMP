from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from modules import languages
from config import env

router = APIRouter(
    prefix="",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="./templates")

@router.get("/", summary="Login page")
def login_page(request: Request):
    return RedirectResponse(url="/admin/", status_code=status.HTTP_302_FOUND)


@router.get("/admin/")
@router.get("/admin/index/{layout:int}/")
async def admin(request: Request, layout:int=env.default_layout) -> templates.TemplateResponse:
    content = {
        'show_layout': True,
        'show_menu': True,
        'path': 'index',
        'layout': layout,
        'labels': await languages.get_labels(env.language),
        'language': env.language
    }
    

    return templates.TemplateResponse("index.html", {"request": request, "content": content})



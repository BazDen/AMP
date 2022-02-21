from fastapi import FastAPI, HTTPException, Request, Depends, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, ORJSONResponse
from jinja2 import PackageLoader, Environment 
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from hashlib import sha256
from database import conn
from models.lang import *
from models.webusers import *
from models.srv import *
from models.groups import *
from models.status import *
from models.tz import *
from models.vocabulary import *
from env import secret



async def to_login(request, exc):
    return templates.TemplateResponse("login.html", {"request": request, })

exceptions = {
    404: to_login,
    401: to_login,
}

app = FastAPI(title='AMP', description='APIs for AMP', version='0.1', exception_handlers=exceptions)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
manager = LoginManager(secret, token_url='/auth/token', use_cookie=True, default_expiry=timedelta(hours=12))
manager.cookie_name = 'amp'

    
@app.get("/", response_class=HTMLResponse, summary="Login page")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, })

async def make_base_content(user):
    content=dict()
    content['labels'] = await get_labels(await get_lang(user.lang))
    content['user'] = user
    content['srvname'] = await get_srv_name()
    return content

@app.get("/admin/", response_class=HTMLResponse, summary="Main admin page")
@app.get("/admin/index/", response_class=HTMLResponse, summary="Main admin page", tags=['Dashboard'])
async def admin(request: Request, user=Depends(manager)):
    content=await make_base_content(user)
    content['show_layout'] = True
    content['path'] = 'index'
    content['layout'] = get_layout(user.id, content['path'])
    return templates.TemplateResponse("index.html", {"request": request, "content": content})
    
    
@app.get("/admin/users/", response_class=HTMLResponse, summary="Users management", tags=['Users'])
async def admin(request: Request, user=Depends(manager)):
    if int(user.status) == 1:
        content=await make_base_content(user)
        content['show_layout'] = False
        content['path'] = 'users'
        content['groups'] = await list_groups(user.status, user.group)
        content['users'] = list_users()
        content['status'] = list_status(await get_lang(user.lang))
        content['tz'] = await list_tz()
        content['lang'] = await list_lang()
        return templates.TemplateResponse("index.html", {"request": request, "content": content})
    else:
        return RedirectResponse(url="/admin/dashboard/",status_code=status.HTTP_302_FOUND)    
    

@app.get("/admin/settings/", response_class=HTMLResponse, summary="Settings page", tags=['Settings'])
async def admin(request: Request, user=Depends(manager)):
    content=await make_base_content(user)
    content['show_layout'] = False
    content['path'] = 'settings'
    content['groupname'] = ''
    gl = await list_groups(user.status, user.group)
    for g in gl:
        if int(g.id) == user.group:
            content['groupname'] = g.name
    content['userstatus'] = ''
    sl = list_status(await get_lang(user.lang))
    for s in sl:
        if s['id'] == int(user.status):
            content['userstatus'] = s['name']
    content['user_status'] = user.status
    content['usertz'] = await get_tz(user.tz)
    if int(user.status) == 1:
        content['srvtz'] = await get_srv_tz()
        content['srvtz_name'] = await get_tz(content['srvtz'])
    content['status'] = list_status(await get_lang(user.lang))
    content['tz'] = await list_tz()
    content['lang'] = await list_lang()
    content['groups'] = await list_groups(user.status, user.group)
    return templates.TemplateResponse("index.html", {"request": request, "content": content})
    
    
@app.get('/setlayout/{layout}/{path}', response_class=HTMLResponse, summary="Set layout on page", tags=['View'])
async def setlayout(layout:int, path: str, user=Depends(manager)):
    await set_layout(user, layout, path)
    return RedirectResponse(url="/admin/",status_code=status.HTTP_302_FOUND)


@app.post('/group/', response_class=HTMLResponse, summary="Edit group", tags=['Groups'])
async def groupedit(
    id: int = Form('id'), 
    type: str = Form('type'),
    path: str = Form('path'),
    name: str = Form('name'),
    user=Depends(manager)):
    if int(user.status)==1:
        if type =='edit':
            await group_edit(id, name)
        elif type =='new':
            await group_add(name)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp


@app.post('/group/remove/', response_class=HTMLResponse, summary="Remove group", tags=['Groups'])
async def groupremove(id: int = Form('id'), path: str = Form('path'), user=Depends(manager)):
    if int(user.status)==1:
        await group_remove(id)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp
    

@app.post('/user/', response_class=HTMLResponse, summary="Edit user", tags=['Users'])
async def useredit(
    id: int = Form('id'), 
    type: str = Form('type'),
    path: str = Form('path'),
    username: str = Form('username'),
    fullname: str = Form('fullname'),
    password: str = Form('password'),
    u_status: int = Form('u_status'),
    group: int = Form('group'),
    tz: int = Form('tz'),
    lang: int = Form('lang'),
    user=Depends(manager)):
    if type =='edit':
        await user_edit(id, username, fullname, u_status, group, tz, user.status, lang)
    elif type =='new':
        if int(user.status)==1:
            await user_add(username, fullname, sha256(password.encode('utf-8')).hexdigest(), u_status, group, tz, lang)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp


@app.post('/user/remove/', response_class=HTMLResponse, summary="Delete user", tags=['Users'])
async def groupremove(id: int = Form('id'), path: str = Form('path'), user=Depends(manager)):
    if int(user.status)==1:
        await user_remove(id)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp


@app.post('/user/change_password/', response_class=HTMLResponse, summary="Change user password", tags=['Users'])
async def user_changepass(id: int = Form('id'), password: str = Form('password'), path: str = Form('path'), user=Depends(manager)):
    if int(user.status)==1:
        await user_change_password(id, sha256(password.encode('utf-8')).hexdigest())
    elif int(user.id)==id:
        await user_change_password(id, sha256(password.encode('utf-8')).hexdigest())
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp
  
@app.post('/tools/srvtz/', response_class=HTMLResponse, summary="Change backend timezone", tags=['Tools'])
async def change_srvtz(typetz: str = Form('type'), tz: int = Form('tz'), path: str = Form('path'), user=Depends(manager)):
    if typetz=='srv':
        if int(user.status)==1:
            await set_srv_tz(tz)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp    
    
@app.post('/tools/srvname/', response_class=HTMLResponse, summary="Change server name", tags=['Tools'])
async def change_srvname(srvname: str = Form('srvname'), path: str = Form('path'), user=Depends(manager)):
    if int(user.status)==1:
        await set_srv_name(srvname)
    resp = RedirectResponse(url="/admin/"+str(path)+"/",status_code=status.HTTP_302_FOUND)
    return resp  


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/login', tags=['Users'])
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = sha256(data.password.encode('utf-8')).hexdigest()
    user = load_user(username)  # we are using the same function to retrieve the user
    if not user:
         return RedirectResponse(url="/login",status_code=status.HTTP_302_FOUND)
    elif password != user.password_sha256:
        return RedirectResponse(url="/login",status_code=status.HTTP_302_FOUND)
    if int(user.status) == 4:
        return RedirectResponse(url="/login",status_code=status.HTTP_302_FOUND)
    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    resp = RedirectResponse(url="/admin",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)

    #templates = Jinja2Templates(directory="templates/en")
    return resp
    #return access_token
    
@app.post('/auth/token', tags=['Users'])
def token(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = sha256(data.password.encode('utf-8')).hexdigest()
    user = load_user(username)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user.password_sha256:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    return access_token
    

@manager.user_loader()
def load_user(username: str):  # could also be an asynchronous function
    user = get_user(username)
    return user
    
    
@app.on_event("startup")
async def startup():
    if conn.is_closed():
        conn.connect()
    
@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()


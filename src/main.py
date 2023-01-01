from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.database import db_connection
from modules import *

app = FastAPI(title='AMP', description='AMP', version='0.3')
app.mount("/static", StaticFiles(directory="./static"), name="static")

app.include_router(dashboard.router)


@app.on_event("startup")
async def startup():
    if db_connection.is_closed():
        db_connection.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not db_connection.is_closed():
        db_connection.close()

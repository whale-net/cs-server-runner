from fastapi import FastAPI

from .routers import basic
from .routers import command

app = FastAPI()
app.include_router(basic.router)
app.include_router(command.router)

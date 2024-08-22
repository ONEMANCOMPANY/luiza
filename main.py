import requests
import uvicorn
import os
from typing import Any, List, Optional
from fastapi import (
    Path, 
    Request, 
    status, 
    Query,
    
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from routers import router as api_routes
from internal.dependencies import app, SECRET_KEY
from internal.database import PostgreSql, Base
from sqlalchemy.ext.declarative import declarative_base


URL_local = "http://localhost:8000"
origins = ["*"]

# Base = declarative_base()
postgresql = PostgreSql(
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432,
    database="luiza"
)
Base.metadata.create_all(bind=postgresql.get_engine())

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    DBSessionMiddleware, 
    db_url='postgresql://postgres:postgres@localhost/luiza'
)
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY, 
    same_site="Lax"
)
app.include_router(api_routes)
print(f'{app.routes}')

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True
    )

from fastapi import FastAPI
from server.query_route import router as query_router
from server.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from server.models import Base, engine, SessionLocal, DATABASE_URL
import os
from sqlalchemy import inspect

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Policy Document Query Service!"}

# Include the routers
app.include_router(query_router, tags=["Query Handler"])
app.include_router(auth_router, tags=["Authentication"])

import os
import uvicorn
port = int(os.environ.get("PORT", 10000))
uvicorn.run("main:app", host="0.0.0.0", port=port)

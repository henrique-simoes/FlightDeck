from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .db import run_migrations
from .personas import ensure_personas_seeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    ensure_personas_seeded()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="FlightDeck API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()

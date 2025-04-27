from fastapi import FastAPI
from app.routes import instrument_routes, auth_routes

app = FastAPI(
    title="Musical Instruments API",
    description="Manage your musical instruments easily!",
    version="1.0.0",
)

app.include_router(auth_routes.router)
app.include_router(instrument_routes.router)

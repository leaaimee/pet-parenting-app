from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import engine, Base

from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.invitations_routes import router as invitations_router



app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield




@app.get("/")
async def root_check():
    return {"message": "Pet Parenting API is live"}



app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])
app.include_router(pets_router, prefix="/api/v2/pets", tags=["Pets"])
app.include_router(invitations_router, prefix="/api/v2/invitations", tags=["Invitations"])


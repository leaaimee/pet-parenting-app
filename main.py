from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import engine, Base

from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.invitations_routes import router as invitations_router


from backend.services.users_service import create_fake_user



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root_check():
    return {"message": "Pet Parenting API is live"}



# try 2 - skip it all

# from fastapi.openapi.utils import get_openapi
#
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     schema = get_openapi(
#         title="Your API",
#         version="1.0.0",
#         description="...",
#         routes=app.routes,
#     )
#     schema["components"]["securitySchemes"] = {
#         "FakeAuth": {"type": "http", "scheme": "bearer"}
#     }
#     schema["security"] = [{"FakeAuth": []}]
#     app.openapi_schema = schema
#     return app.openapi_schema
#
# app.openapi = custom_openapi



app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])
app.include_router(pets_router, prefix="/api/v2/pets", tags=["Pets"])
app.include_router(invitations_router, prefix="/api/v2/invitations", tags=["Invitations"])


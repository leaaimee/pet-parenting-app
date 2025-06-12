from fastapi import FastAPI
import os
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from backend.database import engine, Base

from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.invitations_routes import router as invitations_router

from backend.auth.auth import AUTH0_DOMAIN

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# app = FastAPI(lifespan=lifespan)


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "clientId": AUTH0_CLIENT_ID,
        "appName": "Pet Parenting App",
        "scopes": "openid profile email",
        "usePkceWithAuthorizationCodeGrant": True,
    },
)


@app.get("/")
async def root_check():
    return {"message": "Pet Parenting API is live"}




def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Pet Parenting API",
        version="1.0.0",
        description="API documentation for the Pet Parenting project with Auth0 login.",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": f"https://{AUTH0_DOMAIN}/authorize",
                    "tokenUrl": f"https://{AUTH0_DOMAIN}/oauth/token",
                    "scopes": {
                        "openid": "OpenID Connect scope",
                        "profile": "Profile scope",
                        "email": "Email scope"
                    }
                }
            }
        }
    }

    openapi_schema["security"] = [{"BearerAuth": ["openid", "profile", "email"]}]

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": ["openid", "profile", "email"]}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi



app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])
app.include_router(pets_router, prefix="/api/v2/pets", tags=["Pets"])
app.include_router(invitations_router, prefix="/api/v2/invitations", tags=["Invitations"])


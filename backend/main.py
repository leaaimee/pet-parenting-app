from fastapi import FastAPI

from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.invitations_routes import router as invitations_router



app = FastAPI()


app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])
app.include_router(pets_router, prefix="/api/v2/pets", tags=["Pets"])
app.include_router(invitations_router, prefix="/api/v2/invitations", tags=["Invitations"])


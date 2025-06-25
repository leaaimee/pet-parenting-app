from datetime import timedelta

from typing import Annotated

from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.auth2 import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from backend.database import get_async_session

from backend.schemas.user_schema import Token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.medical_routes import router as medical_router
from backend.routes.invitations_routes import router as invitations_router


from fastapi.responses import JSONResponse
from backend.domain.exceptions import NotFoundError, PermissionDeniedError, ConflictError, InternalError

# Temp
from backend.database import engine, Base
from backend.models import users_models, pets_models, medical_models, media_models


app = FastAPI()



# @app.get("/demo", response_model=UserAccountShowSchema)
# async def demo(session: AsyncSession = Depends(get_async_session)):
#     user = await get_user(email="leaaimee2010@gmail.com", session=session)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
#
# @app.get("/debug-user")
# async def debug_user(session: AsyncSession = Depends(get_async_session)):
#     try:
#         result = await session.execute(select(Users).limit(1))
#         user = result.scalar_one_or_none()
#         if user:
#             return {"id": user.id, "email": user.email}
#         return {"message": "No users found"}
#     except Exception as e:
#         return {"error": str(e)}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    print(user)
    print("----------")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # FIXED
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



app.include_router(users_router, prefix="/api/v2", tags=["Users"])
app.include_router(pets_router, prefix="/api/v2", tags=["Pets"])
app.include_router(medical_router, prefix="/api/v2", tags=["Medical"])
app.include_router(invitations_router, prefix="/api/v2", tags=["Invitations"])



@app.exception_handler(NotFoundError)
async def handle_not_found(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(PermissionDeniedError)
async def handle_permission_denied(request, exc):
    return JSONResponse(status_code=403, content={"detail": str(exc)})

@app.exception_handler(ConflictError)
async def handle_conflict(request, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(InternalError)
async def handle_internal_error(request, exc: InternalError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )



from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.auth2 import get_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from backend.database import get_async_session


from backend.schemas.user_schema import Token, UserProfileShowSchema, UserAccountShowSchema, UserPublic

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.routes.users_routes import router as users_router
from backend.routes.pets_routes import router as pets_router
from backend.routes.invitations_routes import router as invitations_router

from sqlalchemy import select
from backend.models.users_models import Users

from fastapi.openapi.utils import get_openapi


app = FastAPI()


# Charles version
# @app.get("/demo", response_model=UserPublic)
# async def demo(session: AsyncSession = Depends(get_async_session)):
#     result = await get_user(email="leaaimee2010@gmail.com", session=session)
#     return result

@app.get("/demo", response_model=UserAccountShowSchema)
async def demo(session: AsyncSession = Depends(get_async_session)):
    user = await get_user(email="leaaimee2010@gmail.com", session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@app.get("/debug-user")
async def debug_user(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Users).limit(1))
        user = result.scalar_one_or_none()
        if user:
            return {"id": user.id, "email": user.email}
        return {"message": "No users found"}
    except Exception as e:
        return {"error": str(e)}


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
        data={"sub": str(user.id)},  # 🔥 FIXED
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



# app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])
app.include_router(users_router, prefix="/api/v2", tags=["Users v2"])
app.include_router(pets_router, prefix="/api/v2", tags=["Pets"])
app.include_router(invitations_router, prefix="/api/v2", tags=["Invitations"])




# we have to talk about this one
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Pet Parenting API",
#         version="1.0.0",
#         description="API for managing users, pets, profiles, and medical data",
#         routes=app.routes,
#     )
#     # ✅ Register the token endpoint manually
#     openapi_schema["paths"]["/token"] = {
#         "post": {
#             "summary": "Get access token",
#             "requestBody": {
#                 "content": {
#                     "application/x-www-form-urlencoded": {
#                         "schema": {
#                             "type": "object",
#                             "properties": {
#                                 "username": {"type": "string"},
#                                 "password": {"type": "string"},
#                             },
#                             "required": ["username", "password"],
#                         }
#                     }
#                 }
#             },
#             "responses": {
#                 "200": {
#                     "description": "Successful login",
#                     "content": {
#                         "application/json": {
#                             "schema": {
#                                 "type": "object",
#                                 "properties": {
#                                     "access_token": {"type": "string"},
#                                     "token_type": {"type": "string"},
#                                 }
#                             }
#                         }
#                     }
#                 },
#                 "401": {"description": "Unauthorized"},
#             }
#         }
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
# app.openapi = custom_openapi  # ✅ assign it
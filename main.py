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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_async_session)
) -> Token:
    user = await  authenticate_user(session, form_data.username, form_data.password)
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
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


app.include_router(users_router, prefix="/api/v2/users", tags=["Users v2"])




from email.policy import default

from fastapi import FastAPI, Depends
from pycparser.ply.yacc import resultlimit
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.auth2 import get_user
from backend.database import get_async_session
from backend.schemas.user_schema import UserProfileShowSchema
from backend.services.helpers.general_helpers import apply_updates



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from backend.auth.auth2 import authenticate_user, create_access_token


from datetime import timedelta


app = FastAPI()



# @app.get("/get")
# async def hello():
#     return "Hello world"
#
#
# @app.get("/demo", response_model=UserProfileShowSchema)
# async def demo(session: AsyncSession = Depends(get_async_session)):
#     result = await get_user(email="leaaimee2010@gmail.com", session=session)
#     return result




ACCESS_TOKEN_EXPIRE_MINUTES = 30  # optionally remove if already in auth2.py

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}



@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

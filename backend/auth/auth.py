from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from urllib.request import urlopen
import json
import os

# Load environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

# Security scheme for FastAPI
bearer_scheme = HTTPBearer()

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


# try 1 - fake it till you make it
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     return {"id": 0, "email": "ellen.ripley@weyland.com"}













# async def get_current_user(request: Request):
#     """
#     Validates the JWT token in the request using Auth0 public keys.
#     Returns decoded payload if valid, otherwise raises HTTP 401.
#     """
#     credentials = await bearer_scheme(request)
#     token = credentials.credentials
#
#     try:
#         unverified_header = jwt.get_unverified_header(token)
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token header")
#
#     try:
#         jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
#         response = urlopen(jwks_url)
#         keys = json.loads(response.read())["keys"]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to fetch JWKS")
#
#     rsa_key = next(
#         (
#             {
#                 "kty": key["kty"],
#                 "kid": key["kid"],
#                 "use": key["use"],
#                 "n": key["n"],
#                 "e": key["e"]
#             }
#             for key in keys
#             if key["kid"] == unverified_header.get("kid")
#         ),
#         None
#     )
#
#     if rsa_key:
#         try:
#             payload = jwt.decode(
#                 token,
#                 rsa_key,
#                 algorithms=ALGORITHMS,
#                 audience=API_AUDIENCE,
#                 issuer=f"https://{AUTH0_DOMAIN}/"
#             )
#             return payload
#         except JWTError:
#             raise HTTPException(status_code=401, detail="Invalid or expired token")
#
#     raise HTTPException(status_code=401, detail="No matching key found")

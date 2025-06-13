from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
import requests

# Load environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

# Security scheme for FastAPI
http_bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    print("🔐 Step 1: Received token:", token[:40], "...")  # Shortened for log clarity

    try:
        # Step 2: Extract header
        unverified_header = jwt.get_unverified_header(token)
        print("📜 Step 2: Unverified JWT header:", unverified_header)

        # Step 3: Fetch JWKS
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks_response = requests.get(jwks_url)
        print("🌐 Step 3: JWKS fetch status:", jwks_response.status_code)
        jwks = jwks_response.json()["keys"]

        # Step 4: Match key
        rsa_key = next(
            (
                {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                for key in jwks
                if key["kid"] == unverified_header.get("kid")
            ),
            None,
        )
        if not rsa_key:
            print("❌ Step 4: No matching RSA key found in JWKS!")
            raise HTTPException(status_code=401, detail="No matching key found")
        print("🔑 Step 4: Matching RSA key found.")

        # Step 5: Decode token
        print("🎯 Step 5: Using audience =", API_AUDIENCE)
        print("🎯 Step 5: Using issuer =", f"https://{AUTH0_DOMAIN}/")
        print("🔬 JWT claims (unverified):", jwt.get_unverified_claims(token))
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        print("✅ Step 5: Token successfully decoded. Payload:", payload)
        return payload

    except JWTError as e:
        print("❗ JWTError during token verification:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    except Exception as e:
        print("❗ General error during get_current_user:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error during authentication"
        )
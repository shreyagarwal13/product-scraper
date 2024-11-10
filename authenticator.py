from fastapi import HTTPException

class Authenticator:
    STATIC_AUTH_TOKEN = "my_static_token"

    @classmethod
    def verify_token(cls, x_token: str = ""):
        if x_token != cls.STATIC_AUTH_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
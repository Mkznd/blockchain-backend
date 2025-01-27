from starlette.requests import Request

from services.jwt_service import decode_access_token


def check_jwt(request: Request):
    if "Authorization" not in request.headers:
        return False

    auth_header = request.headers["Authorization"]
    auth_type, token = auth_header.split(" ")
    if auth_type != "Bearer":
        return False

    # Check token
    payload = decode_access_token(token)

    return payload["sub"]

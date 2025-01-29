import pytest

from services.jwt_service import create_access_token, decode_access_token


def test_create_access_token():
    token = create_access_token({"sub": "1"})
    assert isinstance(token, str)


def test_decode_access_token():
    token = create_access_token({"sub": "1"})
    payload = decode_access_token(token)
    assert payload["sub"] == "1"


def test_invalid_token():
    with pytest.raises(Exception):
        decode_access_token("invalidtoken")

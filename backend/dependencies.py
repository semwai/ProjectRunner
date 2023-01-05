from fastapi import HTTPException, Cookie
from starlette.requests import Request # noqa
from starlette.websockets import WebSocket

from backend.schemas import User


def verify_auth(request: Request) -> User:
    raw_user = request.session.get('user')
    if raw_user:
        return User(email=raw_user['email'])
    else:
        raise HTTPException(400, "Auth failed")


async def verify_auth_websocket(websocket: WebSocket, session: str | None = Cookie(default=None)):
    if session is None:
        await websocket.accept()
        await websocket.send_text("Auth failed")
        await websocket.close(1000, reason="Auth failed")
    return session

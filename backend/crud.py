import os
from fastapi import Body, APIRouter, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from starlette.requests import Request # noqa

from google.oauth2 import id_token # noqa
from google.auth.transport import requests # noqa
from google.auth.exceptions import GoogleAuthError # noqa

from backend.storage.db import Session
from backend.storage import models
from backend.dependencies import verify_auth
from backend.schemas import GetPages, GetPage, User


api = APIRouter()


@api.get("/pages", response_model=GetPages)
async def get_pages(user: User = Depends(verify_auth)):
    with Session() as db:
        data = db.query(models.Page).all()
        return GetPages(data=[p.dict() for p in data])


@api.get("/page/{page_id}", response_model=GetPage)
async def get_page(page_id: int, user: User = Depends(verify_auth)):
    with Session() as db:
        project = db.query(models.Page).get(page_id)
        if project:
            return GetPage(**project.dict())
        raise HTTPException(404, "project not found")


@api.post("/auth", response_model=User)
def authentication(request: Request, token: str = Body(embed=True)):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get('GOOGLE_CLIENT_ID'))
        request.session['user'] = dict({"email": user["email"], "name": user["name"]})
        request.session['token'] = token
        with Session() as db:
            u = db.query(models.User).filter_by(email=user["email"]).first()
            if not u:
                u = models.User(email=user['email'], name=user['name'])
                db.add(u)
                db.commit()
            request.session['user']['access'] = u.access
            return User(email=u.email, name=u.name, access=u.access)

    except GoogleAuthError:
        raise HTTPException(401, "Google auth error")
    except ValueError:
        raise HTTPException(401, "Token verification fails")


@api.get('/me')
def check(request: Request, user: User = Depends(verify_auth)):
    return user
    # raw_user = request.session.get('user')
    # if raw_user:
    #     with Session() as db:
    #         u = db.query(models.User).filter_by(email=user["email"]).first()
    #         if u:
    #             return User(email=u.email, name=u.name, access=u.access)
    #         else:
    #             raise HTTPException(500, "Auth failed")
    # else:
    #     raise HTTPException(401, "Auth failed")


@api.get('/logout')
def logout(request: Request, user: User = Depends(verify_auth)):
    del request.session['user']
    return Response()

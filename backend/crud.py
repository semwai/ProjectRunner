import os
from fastapi import Body, APIRouter, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from starlette.requests import Request # noqa

from google.oauth2 import id_token # noqa
from google.auth.transport import requests # noqa
from google.auth.exceptions import GoogleAuthError # noqa

from backend.storage.db import Session
from backend.storage.models import ProjectStorage
from backend.dependencies import verify_auth
from backend.schemas import GetProjects, GetProject, User


api = APIRouter()


@api.get("/projects", response_model=GetProjects)
async def get_projects(user: User = Depends(verify_auth)):
    with Session() as db:
        data = db.query(ProjectStorage).all()
        return GetProjects(data=[p.dict() for p in data])


@api.get("/project/{project_id}", response_model=GetProject)
async def get_project(project_id: int, user: User = Depends(verify_auth)):
    with Session() as db:
        project = db.query(ProjectStorage).get(project_id)
        if project:
            return GetProject(**project.dict())
        raise HTTPException(404, "project not found")


@api.post("/auth", response_model=User)
def authentication(request: Request, token: str = Body(embed=True)):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get('GOOGLE_CLIENT_ID'))
        request.session['user'] = dict({"email": user["email"]})
        request.session['token'] = token
        return User(email=user['email'])
    except GoogleAuthError:
        raise HTTPException(400, "Google auth error")
    except ValueError:
        raise HTTPException(400, "Token verification fails")


@api.get('/me')
def check(request: Request, user: User = Depends(verify_auth)):
    raw_user = request.session.get('user')
    if raw_user:
        return User(email=raw_user['email'])
    else:
        raise HTTPException(400, "Auth failed")


@api.get('/logout')
def logout(request: Request, user: User = Depends(verify_auth)):
    del request.session['user']
    return Response()

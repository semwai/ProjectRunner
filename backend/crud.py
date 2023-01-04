import os
import fastapi
from fastapi import Body, APIRouter
from fastapi.exceptions import HTTPException
from starlette.requests import Request # noqa

from google.oauth2 import id_token # noqa
from google.auth.transport import requests # noqa
from google.auth.exceptions import GoogleAuthError # noqa

from backend import storage
from backend.schemas import GetProjects, GetProject, User


api = APIRouter()


@api.get("/projects", response_model=GetProjects)
async def get_projects():
    return storage.projects


@api.get("/project/{project_id}", response_model=GetProject)
async def get_project(project_id: int):
    try:
        project = [project for project in storage.projects.data if project.id == project_id][0]
        return project.dict(exclude_none=True)
    except IndexError:
        raise fastapi.HTTPException(status_code=404, detail="project not found")


@api.post("/auth", response_model=User)
def authentication(request: Request, token: str = Body(embed=True)):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get('GOOGLE_CLIENT_ID'))
        request.session['user'] = dict({"email": user["email"]})
        return User(email=user['email'])
    except GoogleAuthError:
        raise HTTPException(400, "Google auth error")
    except ValueError:
        raise HTTPException(400, "Token verification fails")


@api.get('/me')
def check(request: Request):
    raw_user = request.session.get('user')
    print(raw_user)
    if raw_user:
        return User(email=raw_user['email'])
    else:
        raise HTTPException(400, "Auth failed")

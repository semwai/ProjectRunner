import os

from fastapi import Body, APIRouter, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request  # noqa

from google.oauth2 import id_token  # noqa
from google.auth.transport import requests  # noqa
from google.auth.exceptions import GoogleAuthError  # noqa

from backend.storage.db import Session
from backend.storage import models
from backend.dependencies import verify_auth
from backend.schemas import GetPages, GetPage, User, GetProject, GetFullProject

api = APIRouter()


@api.get("/pages", response_model=GetPages)
async def get_pages(user: User = Depends(verify_auth)):
    with Session() as db:
        data = db.query(models.Page).all()
        return GetPages(data=[p.dict() for p in data])


@api.get("/page/{page_id}", response_model=GetPage)
async def get_page(page_id: int, user: User = Depends(verify_auth)):
    with Session() as db:
        page = db.query(models.Page).get(page_id)
        if page:
            return GetPage(**page.dict())
        raise HTTPException(404, "page not found")


@api.post("/page", response_model=GetPage)
async def post_page(page: GetPage, user: User = Depends(verify_auth)):
    if user.access != 'admin':
        raise HTTPException(403, "user")
    with Session() as db:
        if page.id == 0:
            # create new
            new_page = models.Page(description=page.description, version=page.version, visible=False, name=page.name,
                                   container=page.container, short_description=page.short_description,
                                   scenario=page.scenario, ui=page.ui)
            try:
                db.add(new_page)
                db.commit()
            except IntegrityError:
                raise HTTPException(400, "page with this short description already exists")
        else:
            new_page = db.query(models.Page).get(page.id)
            if new_page:
                new_page.description = page.description
                new_page.version = page.version
                new_page.visible = page.visible
                new_page.name = page.name
                new_page.container = page.container
                new_page.short_description = page.short_description
                new_page.scenario = page.scenario
                new_page.ui = page.ui
                db.commit()
            else:
                raise HTTPException(404, "page not found")
        return page


@api.delete("/page")
async def delete_page(id: int, user: User = Depends(verify_auth)):
    if user.access != 'admin':
        raise HTTPException(403, "user")
    with Session() as db:
        page = db.query(models.Page).get(id)
        if page:
            db.delete(page)
            db.commit()
            return 1
        raise HTTPException(404, "page not found")


@api.get("/project/{project_id}", response_model=GetProject)
async def get_project(project_id: int, user: User = Depends(verify_auth)):
    with Session() as db:
        project = db.query(models.Project).get(project_id)
        if project:
            if user.access == 'user' and not project.public:
                raise HTTPException(404, "project not found")
            return GetProject(**project.dict())
        raise HTTPException(404, "project not found")


@api.get("/project/{project_id}/json", response_model=GetFullProject)
async def get_project(project_id: int, user: User = Depends(verify_auth)):
    with Session() as db:
        project = db.query(models.Project).get(project_id)
        if project:
            if user.access == 'user' and not project.public:
                raise HTTPException(404, "project not found")
            ids = project.content.Ids()
            pages = db.query(models.Page).filter(models.Page.id.in_(ids)).all()
            return GetFullProject(**project.dict(), pages=[p.dict() for p in pages])
        raise HTTPException(404, "project not found")


@api.get("/projects", response_model=list[GetProject])
async def get_projects(user: User = Depends(verify_auth)):
    with Session() as db:
        if user.access == 'admin':
            data = db.query(models.Project).all()
        else:
            data = db.query(models.Project).filter_by(public=True).all()
        return [p.dict() for p in data]


@api.post("/project", response_model=GetProject)
async def post_project(project: GetProject, user: User = Depends(verify_auth)):
    if user.access != 'admin':
        raise HTTPException(403, "user")
    with Session() as db:

        if project.id == 0:
            # create new
            new_project = models.Project(name=project.name, description=project.description, public=project.public, content=project.content)
            try:
                db.add(new_project)
                db.commit()
            except IntegrityError as e:
                raise HTTPException(400, e.detail)
        else:
            new_project = db.query(models.Project).get(project.id)
            if not new_project:
                raise HTTPException(404, "project not found")
            new_project.name = project.name
            new_project.description = project.description
            new_project.public = project.public
            new_project.content = project.content
            db.commit()

        return new_project.dict()


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

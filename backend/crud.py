import fastapi
from fastapi import APIRouter

from backend import storage
from backend.schemas import GetProjects, GetProject

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

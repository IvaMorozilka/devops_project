from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

# Fix needed for import. Will be removed in docker.
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
# 

import crud.todos as crud
from auth.jwthandler import get_current_user
from schemas.todos import TodoOutSchema, TodoInSchema, UpdateTodo
from schemas.tokens import Status
from schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/todos",
    response_model=List[TodoOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_todos(current_user: UserOutSchema = Depends(get_current_user)):
    return await crud.get_todos(user_id=current_user)


@router.get(
    "/todo/{todo_id}",
    response_model=TodoOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_todo(todo_id: int) -> TodoOutSchema:
    try:
        return await crud.get_todo(todo_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Todo does not exist",
        )


@router.post(
    "/todos", response_model=TodoOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_todo(
    todo: TodoInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> TodoOutSchema:
    return await crud.create_todo(todo, current_user)


@router.patch(
    "/todo/{todo_id}",
    dependencies=[Depends(get_current_user)],
    response_model=TodoOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_todo(
    todo_id: int,
    todo: UpdateTodo,
    current_user: UserOutSchema = Depends(get_current_user),
) -> TodoOutSchema:
    return await crud.update_todo(todo_id, todo, current_user)


@router.delete(
    "/todo/{todo_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_todo(
    todo_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_todo(todo_id, current_user)
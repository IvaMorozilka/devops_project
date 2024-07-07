from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

# Fix needed for import. Will be removed in docker.
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
# 

from database.models import Todos
from schemas.todos import TodoOutSchema
from schemas.tokens import Status


async def get_todos():
    return await TodoOutSchema.from_queryset(Todos.all())


async def get_todo(todo_id) -> TodoOutSchema:
    return await TodoOutSchema.from_queryset_single(Todos.get(id=todo_id))


async def create_todo(todo, current_user) -> TodoOutSchema:
    todo_dict = todo.dict(exclude_unset=True)
    todo_dict["author_id"] = current_user.id
    todo_obj = await Todos.create(**todo_dict)
    return await TodoOutSchema.from_tortoise_orm(todo_obj)


async def update_todo(todo_id, todo, current_user) -> TodoOutSchema:
    try:
        db_todo = await TodoOutSchema.from_queryset_single(Todos.get(id=todo_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} does not exist")

    if db_todo.author.id == current_user.id:
        await Todos.filter(id=todo_id).update(**todo.dict(exclude_unset=True))
        return await TodoOutSchema.from_queryset_single(Todos.get(id=todo_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_todo(todo_id, current_user) -> Status:
    try:
        db_todo = await TodoOutSchema.from_queryset_single(Todos.get(id=todo_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} does not exist")

    if db_todo.author.id == current_user.id:
        deleted_count = await Todos.filter(id=todo_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Todo {todo_id} does not exist")
        return Status(message=f"Deleted todo {todo_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
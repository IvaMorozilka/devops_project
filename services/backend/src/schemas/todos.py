from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

# Fix needed for import. Will be removed in docker.
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
# 

from database.models import Todos

TodoInSchema = pydantic_model_creator(
    Todos, name="TodoIn", exclude=["author_id"], exclude_readonly=True)

TodoOutSchema = pydantic_model_creator(
    Todos, name="Todo", exclude =[
      "modified_at", "author.password", "author.created_at", "author.modified_at"
    ]
)

class UpdateTodo(BaseModel):
    content: Optional[str]
    complete: Optional[bool]
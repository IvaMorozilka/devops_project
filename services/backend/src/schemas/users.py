from tortoise.contrib.pydantic import pydantic_model_creator

# Fix needed for import. Will be removed in docker.
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
# 

from database.models import Users


UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True
)

UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)

UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)
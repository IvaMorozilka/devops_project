from tortoise import models, fields


class Users(models.Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=50, null=True)
    login = fields.CharField(max_length=32, unique = True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

class Todos(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="todo")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    complete = fields.BooleanField(default=False)
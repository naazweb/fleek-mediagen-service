from tortoise import fields
from tortoise.models import Model

class MediaGenerationJob(Model):
    id = fields.UUIDField(pk=True)
    prompt = fields.TextField()
    width = fields.IntField()
    height = fields.IntField()
    model = fields.CharField(max_length=100)
    status = fields.CharField(max_length=20, default="queued")
    output_url = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

from tortoise import fields
from tortoise.models import Model
import uuid

from app.core.consts import JobStatus


class MediaGenerationJob(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    
    prompt = fields.TextField()
    model = fields.CharField(max_length='100', default="realistic-v1")
    width = fields.IntField()
    height = fields.IntField()
    
    status = fields.CharField(max_length=20, default=JobStatus.QUEUED.value)
    retries = fields.IntField(default=0)
    error_message = fields.TextField(null=True)
    
    output_url = fields.TextField(null=True) 

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "media_generation_jobs"

    def __str__(self):
        return f"<MediaJob {self.id} - {self.status}>"

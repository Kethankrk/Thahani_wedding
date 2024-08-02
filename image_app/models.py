from django.db import models
import uuid

class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title




class Files(models.Model):
    FILE_TYPE_CHOICES = {
        "V": "VIDEO",
        "I": "IMAGE"
    }
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    file = models.FileField(upload_to='images/')
    compressed_file = models.FileField(upload_to='compressed/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='sub_files', on_delete=models.SET_NULL, null=True)
    file_type = models.CharField(max_length=1, choices=FILE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
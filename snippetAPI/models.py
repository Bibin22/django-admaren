from django.db import models
from django.contrib.auth.models import User


class TagModel(models.Model):
    tag = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.tag


class SnippetModel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

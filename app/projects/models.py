from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    github = models.URLField(null=True)
    link = models.URLField(null=True)

    def __str__(self):
        return self.name

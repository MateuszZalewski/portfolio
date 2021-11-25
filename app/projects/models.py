from django.db import models


class Tech(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    github = models.URLField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

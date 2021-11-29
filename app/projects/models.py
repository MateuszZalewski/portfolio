from django.db import models
from PIL import Image


class Tech(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)

        img = Image.open(self.logo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    github = models.URLField(blank=True)
    link = models.URLField(blank=True)
    techs = models.ManyToManyField(Tech)
    readme = models.TextField(blank=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name

from django.db import models
# from django import forms


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(CommonInfo):
    """Объект на котором проводят измерения."""
    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Measurement(CommonInfo):
    """Измерение температуры на объекте."""
    value = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # image = forms.fields.ImageField(max_length=200, allow_empty_file=True)

from django.db import models

class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    text = models.TextField()

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    data = models.JSONField()

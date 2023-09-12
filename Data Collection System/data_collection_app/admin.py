from django.contrib import admin
from data_collection_app.models import Form, Question, Response

# Register your models here.
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Response)

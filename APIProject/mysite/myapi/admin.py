from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tags, Activities, FinalResult, Paragraphs

admin.site.register(Tags)
admin.site.register(Activities)
admin.site.register(FinalResult)
admin.site.register(Paragraphs)
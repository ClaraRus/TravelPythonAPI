from django.db import models

# Create your models here.
class Tags(models.Model):
    tags = models.CharField(max_length=100000)

    def __str__(self):
        return self.tags

class Activities(models.Model):
    activities = models.CharField(max_length=100000)

    def __str__(self):
        return self.activities

class FinalResult(models.Model):
    finalresult = models.CharField(max_length=100000)

    def __str__(self):
        return self.finalresult


class Paragraphs(models.Model):
    paragraphs = models.CharField(max_length=100000)

    def __str__(self):
        return self.paragraphs
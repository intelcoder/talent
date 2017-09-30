from django.db import models

class Timestampable(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  delated_at = models.DateTimeField(auto_now=True)
    
  class Meta:
    abstract = True  # <--- denotes our model as abstract


class AbstractArea(models.Model):
  name = models.CharField(max_length=150)
  lat = models.FloatField()
  lng = models.FloatField()

  class Meta:
    abstract = True


class AbstractReview(Timestampable, models.Model):
  content = models.CharField(max_length=255)

  class Meta:
    abstract = True  # <--- denotes our model as abstract

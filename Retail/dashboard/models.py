from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='inactive')

    def __str__(self):
        return self.name

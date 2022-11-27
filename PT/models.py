from django.db import models

class User(models.Model):
    userID = models.TextField(primary_key=True)
    userPW = models.TextField()
    userName = models.TextField()

class InterestPlant(models.Model):
    userID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    plantID = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userID', 'plantID'], name='Do not allow duplication'),
        ]
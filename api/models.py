from django.db import models


class Message(models.Model):
    id=models.IntegerField(auto_created=True, primary_key=True)
    person = models.CharField(max_length=30)
    text = models.TextField()
    subText = models.CharField(blank=True, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person+self.text
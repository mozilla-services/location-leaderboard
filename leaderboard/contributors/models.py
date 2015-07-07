from django.db import models


class Contributor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

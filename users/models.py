from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class PrivilegesUserAdmin(models.Model):
    privileges = models.ForeignKey('surveys.Privileges', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("privileges", "user"),)

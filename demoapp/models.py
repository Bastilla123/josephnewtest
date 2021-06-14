from django.db import models
from django.contrib.auth.models import User

class Properties(models.Model):
    name = models.CharField(max_length=120, default="", blank=True, null=True)

class Address(models.Model):
    birthdate = models.DateField(default=None, blank=True, null=True)
    country = models.PositiveSmallIntegerField(choices=((0,'Deutschland')), blank=True, default=0, null=True)
    user_link = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None,
                                    related_name="%(class)s_owner", )
    properties_link = models.ManyToManyField(Properties, default=None,)
    def __str__(self):
        return self.get_status_display()

class Estates(models.Model):
    name = models.CharField(max_length=120, default="", blank=True, null=True)
    datetimefield = models.DateTimeField(blank=True, null=True,default=None)
    estateowner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None,
                              related_name="%(class)s_owner", )
    address_link = models.ManyToManyField(Address, default=None,)

    def __str__(self):
        return self.name

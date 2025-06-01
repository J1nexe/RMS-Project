from django.db import models # type: ignore

class UserLogin(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class studentRecord(models.Model):
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    yearAndSection = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.
class My_users(models.Model):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    email=models.CharField(max_length=50)


class File(models.Model):
    username=models.CharField(max_length=90)
    filename=models.CharField(max_length=90)
    filename_real=models.CharField(max_length=90)
    url=models.CharField(max_length=100)


class Backup(models.Model):
    username=models.CharField(max_length=90)
    filename=models.CharField(max_length=90)
    filename_real=models.CharField(max_length=90)
    url=models.CharField(max_length=100)


class SharedFiles(models.Model):
    sender_name=models.CharField(max_length=90)
    receiver_name=models.CharField(max_length=90)
    bucket_name=models.CharField(max_length=90)
    sender_email=models.CharField(max_length=90)
    receiver_email=models.CharField(max_length=90)
    shared_filename=models.CharField(max_length=90)
    real_filename=models.CharField(max_length=90)

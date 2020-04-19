from django.contrib import admin
from core import models
# Register your models here.
class Admin_My_User(admin.ModelAdmin):
    lsit_display=['username','email','username','firstname','lastname']
admin.site.register(models.My_users,Admin_My_User)

class AdminsFiles(admin.ModelAdmin):
    list_display=['username','filename','filename_real','url']

admin.site.register(models.File,AdminsFiles)


class AdminsBackup(admin.ModelAdmin):
    list_display=['username','filename','filename_real','url']

admin.site.register(models.Backup,AdminsBackup)

class AdminsShared(admin.ModelAdmin):
    list_display=['sender_name','receiver_name','bucket_name','sender_email','receiver_email','shared_filename','real_filename']

admin.site.register(models.SharedFiles,AdminsShared)

from django.contrib import admin
from profiles_api import models

admin.site.register(models.UserProfile)
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Image)
admin.site.register(models.Video)
admin.site.register(models.Review)
admin.site.register(models.Instructor)

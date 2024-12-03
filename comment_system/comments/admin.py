from django.contrib import admin
from .models import CustomUser, Course,Alumni

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Alumni)
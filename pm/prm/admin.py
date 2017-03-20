from django.contrib import admin

from .models.project import Project
from .models.user import User
from .models.member import Member

# Register your models here.


admin.site.register(Project)
admin.site.register(User)
admin.site.register(Member)
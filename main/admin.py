from django.contrib import admin
from .models import Comments, BlogPost

admin.site.register(BlogPost)
admin.site.register(Comments)


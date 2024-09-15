from django.contrib import admin
from .models import Meme, Comment, SystemMessage

admin.site.register(Meme)
admin.site.register(Comment)
admin.site.register(SystemMessage)
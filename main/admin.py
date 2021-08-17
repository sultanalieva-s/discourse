from django.contrib import admin

# Register your models here.
from main.models import *

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(Reply)

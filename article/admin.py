from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ArticlePost
from .models import ArticleColumn
#注册ArticlePost到admin中，用后台管理ArticlePost这个数据表
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)
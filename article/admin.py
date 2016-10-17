from django.contrib import admin
from .models import Article,File

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

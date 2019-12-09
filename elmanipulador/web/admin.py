from django.contrib import admin
from .models import Author, Article

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

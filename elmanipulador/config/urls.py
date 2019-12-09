from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('', views.home),
    path('articles/<int:article_id>/', views.article),
    path('admin/', admin.site.urls),
]

from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import ImageAPIView

urlpatterns = [
    path('image/', ImageAPIView.as_view())
]

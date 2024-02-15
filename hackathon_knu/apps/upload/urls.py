from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import ImageAPIVIew

router = DefaultRouter()
router.register('image', ImageAPIVIew, 'music')


urlpatterns = [
    # path('image/', ImageAPIVIew.as_view(), name='get-tour'),
]



urlpatterns += router.urls


# from django.urls import path
# from .views import index, upload_photo

# urlpatterns = [
#     # path('', index, name='index'),
#     path('upload_photo/', upload_photo, name='upload_photo'),
# ]

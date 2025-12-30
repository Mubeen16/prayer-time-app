from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RafeeqViewSet

router = DefaultRouter()
router.register(r'rafeeq', RafeeqViewSet, basename='rafeeq')

urlpatterns = [
    path('', include(router.urls)),
]

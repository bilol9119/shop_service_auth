from django.urls import path
from .views import TokenViewSet

urlpatterns = [
    path('check/token/', TokenViewSet.as_view({"post": "check_token"})),
    path('create/token/', TokenViewSet.as_view({"post": "create_token"})),
]

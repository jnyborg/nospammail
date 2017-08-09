from django.conf.urls import url, include
from dashboard import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'emails', views.GeneratedEmailViewSet)
router.register(r'users', views.UserViewSet)


# API endpoints
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
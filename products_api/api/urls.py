from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers

from .views import ReviewViewSet, ProductViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'products', ProductViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'products/(?P<products_pk>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]

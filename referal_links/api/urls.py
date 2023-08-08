from django.urls import path, include
from .views import (SendAuthCodeView, CheckPhoneAuthCodeView,
                    ProfileViewSet)
from rest_framework.routers import DefaultRouter


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register('users', ProfileViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('send_auth_code', SendAuthCodeView.as_view(), name='send-code'),
    path('check_phone_code',
         CheckPhoneAuthCodeView.as_view(),
         name='check-phone-code')
]

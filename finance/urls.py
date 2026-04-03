from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FinancialRecordViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'records', FinancialRecordViewSet, basename='record')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]

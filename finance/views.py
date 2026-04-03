from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, FinancialRecord
from .serializers import UserSerializer, FinancialRecordSerializer
from .permissions import IsAdminRole, IsAdminOrAnalystReadOnly, DashboardAccessPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]

class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAdminOrAnalystReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'category', 'date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [DashboardAccessPermission]

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        records = FinancialRecord.objects.all()
        income = records.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = records.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'total_income': income,
            'total_expenses': expense,
            'net_balance': income - expense
        })

    @action(detail=False, methods=['get'], url_path='category-summary')
    def category_summary(self, request):
        category_data = FinancialRecord.objects.values('category', 'type').annotate(total_amount=Sum('amount')).order_by('category')
        return Response(category_data)

    @action(detail=False, methods=['get'], url_path='monthly-trends')
    def monthly_trends(self, request):
        monthly_data = FinancialRecord.objects.annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total_amount=Sum('amount')
        ).order_by('month')
        return Response(monthly_data)

    @action(detail=False, methods=['get'], url_path='recent')
    def recent(self, request):
        recent_records = FinancialRecord.objects.order_by('-created_at')[:10]
        serializer = FinancialRecordSerializer(recent_records, many=True)
        return Response(serializer.data)

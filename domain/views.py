from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from domain.models import Statement, Category
from domain.serializers.category_serializer import CategorySerializer
from domain.serializers.statement_serializer import StatementSerializer


# Create your views here.


@api_view(['POST'])
def create_statement(request):
    serializer = StatementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_all_statement(request):
    statements = Statement.objects.all()
    serializer = StatementSerializer(statements, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_all_category(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=200)

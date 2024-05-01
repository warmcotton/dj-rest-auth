from rest_framework import serializers

from domain.enum.category_field import CategoryType
from domain.models import Statement, Category
from domain.serializers.category_serializer import CategorySerializer


class StatementSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Statement
        fields = ['level', 'text', 'category']

    def create(self, validated_data):
        print("create 실행")
        category_data = validated_data.pop('category')
        if not category_data:
            raise ValueError("카테고리 정보 없음")
        else:
            statement = Statement.objects.create(**validated_data)
            for data in category_data:
                category = Category.objects.create(category=CategoryType(data), statement=statement)
                category.save()
            return statement
from rest_framework import serializers

from domain.enum.category_field import CategoryType
from domain.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']

    def to_representation(self, instance):
        return instance.category.value


    def to_internal_value(self, data):
        return data
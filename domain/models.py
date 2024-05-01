from enum import Enum, auto

from django.db import models

from domain.enum.category_field import EnumField, CategoryType


# Create your models here.


class Statement(models.Model):
    level = models.IntegerField()
    text = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    category = EnumField(CategoryType, null=False, blank=False)
    statement = models.ForeignKey(Statement, null=False, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return str(self.category.value)

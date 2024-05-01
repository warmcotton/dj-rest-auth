from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models


class CategoryType(Enum):
    NOUNS = 'NOUNS'
    VERBS = 'VERBS'
    ADJECTIVES = 'ADJECTIVES'
    ADVERBS = 'ADVERBS'


class EnumField(models.CharField):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        self.__enum_value_to_key_map = {item.value: item for item in self.enum}
        if not issubclass(self.enum, Enum):
            raise TypeError('enum 인자는 Enum 형식이여야 합니다.')
        kwargs["max_length"] = 104
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['enum'] = self.enum
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, self.enum):
            return value
        if value is None:
            return None
        val = self.__enum_value_to_key_map[value]
        if val is None:
            raise Exception('존재하지 않는 Enum 타입입니다.')
        return val

    def from_db_value(self, value, expression, connection):
        return self.to_python(value=value)

    def get_prep_value(self, value):
        if isinstance(value, self.enum):
            return value.value
        else:
            return value

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not isinstance(value, self.enum):
            raise ValidationError('잘못된 Enum 타입입니다.')

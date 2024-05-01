from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False)
    sex = serializers.CharField(max_length=1, required=False)
    def save(self, request):
        user = super().save(request)
        user.sex = self.data.get('sex')
        user.age = self.data.get('age')
        user.save()
        return user
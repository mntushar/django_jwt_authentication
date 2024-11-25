from rest_framework import serializers

from backend.account.authentication.models import Login


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

    def create(self, validated_data):
        return Login(**validated_data)

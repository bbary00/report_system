from rest_framework_mongoengine import serializers as me_serializers
from rest_framework import serializers
from templates.api.models import Template, Report
from django.contrib.auth import get_user_model


class TemplateSerializer(me_serializers.DocumentSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['date', 'user']


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=200)


class ReportSerializer(me_serializers.DocumentSerializer):

    class Meta:
        model = Report
        read_only_fields = ['user', 'date']


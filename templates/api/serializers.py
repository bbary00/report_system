from rest_framework_mongoengine import serializers as me_serializers
from templates.api.models import Template, Report
from rest_framework import serializers


class TemplateSerializer(me_serializers.DocumentSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['date', 'user']


class ReportSerializer(me_serializers.DocumentSerializer):

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['user', 'date']


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=200)


from rest_framework_mongoengine import viewsets
from templates.api.serializers import ToolSerializer
from templates.api.models import Tool


class ToolViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def get_queryset(self):
        return Tool.objects.all()

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)

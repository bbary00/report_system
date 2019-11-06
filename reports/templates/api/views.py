from rest_framework import status
from rest_framework.response import Response
from templates.api.serializers import TemplateSerializer, UserSerializer, ReportSerializer
from templates.api.models import Template, Report
from rest_framework_mongoengine import viewsets
from rest_framework.views import APIView
from mongo_auth.permissions import AuthenticatedOnly


class TemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedOnly]
    lookup_field = 'id'
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserAPIView(APIView):
    permission_classes = [AuthenticatedOnly]

    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedOnly]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def create(self, request, *args, **kwargs):
        template = request.data.get('template', {})
        template_id = template.get('id', {})
        if not template_id:
            return Response({"error": "Template id is not provided"})

        template_object = Template.objects.filter(id=template_id)
        if template_object.count() == 1:
            report_object = request.data
            if len(template_object[0]['inputs']) != len(report_object['answers']):
                return Response({"error": f"Provided wrong number of inputs. Should be "
                                          f"{len(template_object[0]['inputs'])}"})
            report_object['template'] = TemplateSerializer(template_object[0]).data
            serializer = self.get_serializer(data=report_object)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "Template not found"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

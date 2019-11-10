from templates.api.serializers import TemplateSerializer, UserSerializer, ReportSerializer
from mongo_auth.permissions import AuthenticatedOnly, IsUserAdminOrReadOnly, IsUserAdmin
from templates.api.models import Template, Report
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import status
import xlwt


class TemplateViewSet(viewsets.ModelViewSet):
    """
    Retrieve and create template
    Permission to create only for admins
    """
    permission_classes = [AuthenticatedOnly, IsUserAdminOrReadOnly]
    lookup_field = 'id'
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def create(self, request, *args, **kwargs):
        print("!!!!!!")
        if any([not val for val in request.data.values()]):
            return Response(data={"data": {"error": "Please provide all fields!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        label = request.data.get('label')
        template_object = Template.objects.filter(label=label)
        if template_object.count() > 0:
            return Response(data={"data": {"error": "Template with this label exists!"}},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserAPIView(APIView):
    """
    See current user information
    """
    permission_classes = [AuthenticatedOnly]

    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    """
    Create and retrieve reports
    """
    permission_classes = [AuthenticatedOnly]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def create(self, request, *args, **kwargs):
        # To create a report need provide template id
        # "template": {"id": "132sa1d65asd35a1sd"}
        template = request.data.get('template', {})
        template_id = template.get('id', {})
        if not template_id:
            return Response({"error": "Template id is not provided"}, status=status.HTTP_403_FORBIDDEN)

        # Find template with provided id
        template_object = Template.objects.filter(id=template_id)
        if template_object.count() == 1:
            report_object = request.data
            # If number of fields in template not equal to provided answers - error
            if len(template_object[0]['inputs']) != len(report_object['answers']):
                return Response(data={"data": {"error": f"Provided wrong number of inputs. "
                                                        f"Should be {len(template_object[0]['inputs'])}"}})

            # Add template object to report
            report_object['template'] = TemplateSerializer(template_object[0]).data
            serializer = self.get_serializer(data=report_object)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        # Add user object to report
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # If user is admin return all reports
        # If admin user provide username - return reports of provided username
        if self.request.user['is_staff'] or self.request.user['is_staff']:
            query = self.request.GET.get('user')
            if query:
                qs = self.queryset.filter(user__username=query)
                return qs
            return self.queryset
        # Else return reports of current user
        print(self.request.user)
        return self.queryset.filter(user__username=self.request.user["username"])


# @permission_required([IsUserAdmin, AuthenticatedOnly])
# def export_reports(request):
class LoadViewSet(APIView):
    """
    Create and retrieve reports
    """
    permission_classes = [AuthenticatedOnly, IsUserAdmin]

    def get(self, request):
        """Download all reports if user is admin"""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Reports.xls"'
        # creating workbook
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Reports")
        row_num = 0
        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True
        # column header names, you can use your own headers here
        columns = ['Username', 'Email', 'Template Name', 'Inputs', 'Answers', 'Date']
        # write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        data = ReportSerializer(Report.objects.all(), many=True).data
        for obj in data:
            row_num += 1
            ws.write(row_num, 0, obj['user']['username'], font_style)
            ws.write(row_num, 1, obj['user']['email'], font_style)
            ws.write(row_num, 2, obj['template']['label'], font_style)
            ws.write(row_num, 3, ', '.join(obj['template']['inputs']), font_style)
            ws.write(row_num, 4, ', '.join(obj['answers']), font_style)
            ws.write(row_num, 5, obj['date'], font_style)

        wb.save(response)
        return response


from templates.api.views import (TemplateViewSet, UserAPIView, ReportViewSet, export_reports)
from rest_framework_mongoengine import routers
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'templates', TemplateViewSet, base_name='template')
router.register(r'reports', ReportViewSet, base_name='reports')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'user/', UserAPIView.as_view()),
    path(r'load/', export_reports)
]
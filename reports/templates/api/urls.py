from rest_framework_mongoengine import routers
from templates.api.views import (TemplateViewSet, UserAPIView, ReportViewSet)
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'templates', TemplateViewSet, base_name='template')
router.register(r'reports', ReportViewSet, base_name='reports')

# router.register(r'reports', ReportViewSet, base_name='report')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'user/', UserAPIView.as_view())
]
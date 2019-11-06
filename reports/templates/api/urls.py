from rest_framework_mongoengine import routers
from templates.api.views import ToolViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'mongo', ToolViewSet, base_name='template')

urlpatterns = [
    path(r'', include(router.urls))
]
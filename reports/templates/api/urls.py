from rest_framework import routers
from templates.api.views import ToolViewSet

router = routers.DefaultRouter()
router.register(r'mongo', ToolViewSet)

urlpatterns = []

urlpatterns += router.urls

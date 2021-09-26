
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from measurements import views

router_projects = DefaultRouter()
router_projects.register('', views.ProjectViewSet)
router_measurements = DefaultRouter()
router_measurements.register('', views.MeasurementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/projects/', include(router_projects.urls)),
    path('api/v1/measurements/', include(router_measurements.urls))
]

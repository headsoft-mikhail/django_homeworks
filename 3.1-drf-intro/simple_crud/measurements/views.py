from rest_framework.viewsets import ModelViewSet
from measurements.models import Project, Measurement
from measurements.serializers import ProjectSerializer, MeasurementSerializer

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class MeasurementViewSet(ModelViewSet):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()
